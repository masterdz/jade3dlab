"""Jade Engine AI Script Extractor & Decompiler.

Decompiles binary AI script bytecodes (.ofc, .fct, .omd, .mdl, .ova, .oin, and WOW type 4/7 entries)
into readable C-like Jade scripts and assembly listings.
Based on Jade Engine's official AIinterp VM architecture:
  - Keywords: AIdefkey.h (88 opcodes)
  - Data Types: AIdeftyp.h (28 types)
  - Fields: AIdeffields.h (35 object/message fields)
  - Native APIs: AIdeffct.h (1,107 engine functions)
"""
from __future__ import annotations

import os
from pathlib import Path
import re
import struct
from typing import Any, Dict, List, Optional, Set, Tuple


# ============================================================================
# 1. OPCODES & VM DICTIONARIES (Official Jade AIinterp Engine Definitions)
# ============================================================================

CATEGORIES: Dict[int, str] = {
    1: "TYPE",
    2: "KEYWORD",
    3: "FUNCTION",
    4: "FIELD",
    5: "LOCALVAR",
    6: "LOCALVARARRAY",
    7: "LOCALVARARRAY2",
    8: "LOCALVARARRAY3",
    10: "LOCALVARARRAYREF",
    11: "LOCALVARARRAY2REF",
    12: "LOCALVARARRAY3REF",
    20: "GLOBALVAR",
    21: "GLOBALVARARRAY",
    22: "GLOBALVARARRAY2",
    23: "GLOBALVARARRAY3",
    25: "INITLOCALVARARRAY",
    26: "EVENTPARAM",
    27: "POPPROC",
    28: "LOCALVARREF",
    29: "POPPROCREF",
    31: "ENDTREE",
}

TYPES: Dict[int, str] = {
    32: "bool",
    33: "int",
    34: "float",
    37: "vector",
    38: "string",
    39: "function",
    40: "object",
    41: "message",
    42: "model",
    43: "network",
    44: "text",
    45: "key",
    46: "color",
    48: "byref",
    49: "byrefarr",
    50: "messageid",
    51: "trigger",
    124: "void",
    125: "every",
    126: "hexa",
    127: "binary",
    128: "private",
    129: "separator",
    130: "enum",
    131: "save",
    132: "reinit",
    133: "saveal",
    134: "optim",
}

KEYWORDS: Dict[int, str] = {
    2048: "if",
    2049: "else",
    2050: "while",
    2051: "&&",
    2052: "||",
    2053: "meta",
    2054: "ultra",
    2057: "for",
    2058: "procedure",
    2059: "switch",
    2060: "case",
    2061: "default:",
    2062: "procedure_trigger",
    2063: "procedure_local",
    2064: "procedure_ultra",
    2100: "return",
    2101: "break",
    2102: "push",
    2103: "pop",
    2106: "stop",
    2107: "returntrack",
    2108: "continue",
    2109: "call_trigger",
    2110: "call",
    2111: "inprocstack",
    2112: "outprocstack",
    2150: "p=",
    2151: "vp=",
    2152: "mp=",
    2153: "tp=",
    2200: "=",
    2201: "+=",
    2202: "-=",
    2203: "++",
    2204: "--",
    2205: "*=",
    2206: "/=",
    2207: "!",
    2208: "-",
    2209: "==",
    2210: ">=",
    2211: "<=",
    2212: ">",
    2213: "<",
    2214: "!=",
    2215: "+",
    2216: "*",
    2217: "/",
    2218: "^",
    2219: "<<",
    2220: ">>",
    2221: "%",
    2222: "&",
    2223: "|",
    2224: "~",
    2300: "JumpFalse",
    2301: "JumpTrue",
    2302: "Jump",
    2303: "JumpFF",
    2304: "JumpFalseSP",
    2305: "JumpTrueSP",
}

FIELDS: Dict[int, str] = {
    512: ".x",
    513: ".y",
    514: ".z",
    515: ".msg_sender",
    516: ".msg_id",
    517: ".msg_vec1",
    518: ".msg_vec2",
    519: ".msg_vec3",
    520: ".msg_vec4",
    521: ".msg_vec5",
    527: ".msg_gao1",
    528: ".msg_gao2",
    529: ".msg_gao3",
    530: ".msg_gao4",
    531: ".msg_gao5",
    532: ".msg_int1",
    533: ".msg_int2",
    534: ".msg_int3",
    535: ".msg_int4",
    536: ".msg_int5",
    550: ".des_flags",
    551: ".des_int1",
    552: ".des_int2",
    553: ".des_float1",
    554: ".des_float2",
    555: ".des_vec1",
    556: ".des_vec2",
    557: ".des_object1",
    558: ".des_object2",
    559: ".des_net1",
}

# Key Native Engine Functions (1100+ native APIs across mechanics, physics, and combat)
FUNCTIONS: Dict[int, str] = {
    4096: "DBG_TraceInt",
    4097: "DBG_TraceFloat",
    4098: "DBG_TraceVector",
    4099: "DBG_TraceString",
    4100: "DBG_BreakPoint",
    4101: "DBG_TraceChar",
    4102: "DBG_TraceObject",
    4103: "DBG_Error",
    4104: "DBG_RenderVector",
    4105: "DBG_EraseAllVectors",
    4118: "DBG_Warning",
    8100: "OBJ_Move",
    8101: "OBJ_Rotate",
    8102: "OBJ_Scale",
    8103: "OBJ_PositionGet",
    8104: "OBJ_PositionSet",
    8105: "OBJ_RotationGet",
    8106: "OBJ_RotationSet",
    8183: "OBJ_HierarchyMoveFather",
    8261: "OBJ_MorphAnimFactor",
    8262: "OBJ_MorphAnimFactorNoKey",
    10000: "DYN_SpeedReachInTime",
    10001: "DYN_SpeedSetVector",
    10002: "DYN_SpeedGetVector",
    10007: "DYN_TractionSet",
    10009: "DYN_FrictionSetForMaxSpeed",
    10011: "DYN_SpeedGet",
    10012: "DYN_SpeedSet",
    10013: "DYN_SpeedLimitGet",
    10014: "DYN_SpeedLimitSet",
    10040: "DYN_SpeedLimitHorizSet",
    10042: "DYN_SpeedLimitVertSet",
    10049: "DYN_SpeedAlignSight",
    10051: "DYN_TractionVectorGet",
    11000: "COL_RayCast",
    11020: "COL_TopPointGet",
    11051: "COL_TipTopPointGet",
    12000: "SND_SoundPlay",
    12001: "SND_SoundStop",
    12075: "SND_TrackStatusGet",
    12081: "SND_TrackSeti",
    12082: "SND_TrackGeti",
    12117: "SND_TrackChain",
    12129: "SND_SoundPlayerForAnimators",
    13000: "ANI_AnimSet",
    13005: "ANI_AnimGet",
    13010: "ANI_ModeGet",
    13011: "ANI_ModeSet",
    13015: "ANI_FrameGet",
    13016: "ANI_FrameSet",
    14000: "CAM_ActiveSet",
    14001: "CAM_TargetSet",
    15000: "TIME_GetDt",
    15001: "TIME_GetTime",
    16000: "MATH_Sin",
    16001: "MATH_Cos",
    16002: "MATH_Distance",
    16003: "MATH_Random",
    17000: "ACT_ActionSet",
    17001: "ACT_ActionGet",
    18000: "AI_Execute",
    18001: "AI_SendMessage",
}


# Populate additional functions dynamically from AIdeffct.h if available
def _load_engine_functions():
    sdk_h = Path(__file__).resolve().parent.parent / "jaded-src" / "src" / "libraries" / "AIinterp" / "Sources" / "Functions" / "AIdeffct.h"
    if sdk_h.is_file():
        try:
            content = sdk_h.read_text(encoding="latin-1", errors="replace")
            for m in re.finditer(r"DEFINE_FUNCTION\s*\(\s*(\d+)\s*,\s*(\w+)\s*,\s*\"([^\"]*)\"", content):
                fid = int(m.group(1))
                name = m.group(3)
                if fid not in FUNCTIONS:
                    FUNCTIONS[fid] = name
        except Exception:
            pass


_load_engine_functions()


# ============================================================================
# 2. DATA STRUCTURES
# ============================================================================

class AINode:
    """An 8-byte Jade AI Virtual Machine bytecode opcode."""
    def __init__(self, index: int, l_param: int, w_param: int, flags: int, c_type: int):
        self.index = index
        self.l_param = l_param
        self.w_param = w_param
        self.flags = flags
        self.c_type = c_type

    @property
    def category_name(self) -> str:
        return CATEGORIES.get(self.c_type, f"CAT_{self.c_type}")

    @property
    def type_name(self) -> str:
        return TYPES.get(self.w_param, f"type_{self.w_param}")

    @property
    def keyword_name(self) -> str:
        return KEYWORDS.get(self.w_param, f"kw_{self.w_param}")

    @property
    def function_name(self) -> str:
        return FUNCTIONS.get(self.w_param, f"Function_{self.w_param}")

    @property
    def field_name(self) -> str:
        return FIELDS.get(self.w_param, f"field_{self.w_param}")

    @property
    def float_value(self) -> float:
        """Decode l_param as IEEE 754 float."""
        try:
            return struct.unpack("<f", struct.pack("<i", self.l_param))[0]
        except Exception:
            return 0.0

    def __repr__(self) -> str:
        return f"Node[{self.index:03d}]: {self.category_name} (w={self.w_param}, l={self.l_param})"


class AIVariable:
    """A variable definition in an AI Model or Function."""
    def __init__(self, offset: int, var_type: int, name: str):
        self.offset = offset
        self.var_type = var_type
        self.name = name

    @property
    def type_str(self) -> str:
        return TYPES.get(self.var_type, "int" if self.var_type > 255 else f"type_{self.var_type}")


class AIFunction:
    """A compiled AI function or procedure bytecode block."""
    def __init__(
        self,
        key: int = 0,
        name: str = "",
        stack_size: int = 0,
        nodes: Optional[List[AINode]] = None,
        strings: Optional[bytes] = None,
        locals_list: Optional[List[AIVariable]] = None,
    ):
        self.key = key
        self.name = name or f"Function_0x{key:08X}"
        self.stack_size = stack_size
        self.nodes = nodes or []
        self.strings = strings or b""
        self.locals = locals_list or []

    def get_string(self, offset: int) -> str:
        """Read null-terminated string literal from string table."""
        if not self.strings or offset < 0 or offset >= len(self.strings):
            return ""
        end = self.strings.find(b"\0", offset)
        if end == -1:
            end = len(self.strings)
        return self.strings[offset:end].decode("latin-1", "replace")


class AIModel:
    """An AI Model defining state logic, functions, and variables for an actor class."""
    def __init__(self, key: int = 0, name: str = ""):
        self.key = key
        self.name = name or f"Model_0x{key:08X}"
        self.function_keys: List[int] = []
        self.procedure_keys: List[int] = []
        self.var_keys: List[int] = []
        self.functions: Dict[int, AIFunction] = {}
        self.variables: List[AIVariable] = []


# ============================================================================
# 3. BINARY PARSERS
# ============================================================================

def parse_ai_function(data: bytes, key: int = 0, name: str = "") -> Optional[AIFunction]:
    """Parse an AI Engine Function (.ofc / .fct) from binary payload."""
    if len(data) < 8:
        return None

    try:
        stack_size, node_val = struct.unpack_from("<II", data, 0)
        # Determine whether node_val is byte count (num_nodes * 8) or direct node count
        if node_val > 0 and node_val % 8 == 0 and 8 + node_val <= len(data):
            num_nodes = node_val // 8
            node_bytes = node_val
        elif node_val > 0 and 8 + node_val * 8 <= len(data):
            num_nodes = node_val
            node_bytes = node_val * 8
        elif len(data) >= 12:
            hdr, s_size, n_val = struct.unpack_from("<III", data, 0)
            if n_val > 0 and (n_val % 8 == 0 or 12 + n_val * 8 <= len(data)):
                stack_size = s_size
                num_nodes = n_val // 8 if n_val % 8 == 0 else n_val
                node_bytes = num_nodes * 8
                data = data[4:]
            else:
                return None
        else:
            return None

        nodes = []
        valid_cats = set(CATEGORIES.keys())
        for i in range(num_nodes):
            offset = 8 + i * 8
            l_param, w_param, flags, c_type = struct.unpack_from("<ihBB", data, offset)
            nodes.append(AINode(i, l_param, w_param, flags, c_type))

        cur = 8 + node_bytes
        # Read optional debug/other root node length
        if cur + 4 <= len(data):
            other_bytes = struct.unpack_from("<I", data, cur)[0]
            cur += 4
            if other_bytes > 0 and cur + other_bytes <= len(data):
                cur += other_bytes

        # Read string buffer
        strings = b""
        if cur + 4 <= len(data):
            str_bytes = struct.unpack_from("<I", data, cur)[0]
            cur += 4
            if 0 < str_bytes <= len(data) - cur:
                strings = data[cur:cur + str_bytes]
                cur += str_bytes

        # Read local variable symbols (if present in uncooked assets)
        locals_list = []
        if cur + 4 <= len(data):
            local_bytes = struct.unpack_from("<I", data, cur)[0]
            cur += 4
            num_locals = local_bytes // 40
            if 0 < num_locals < 200 and cur + num_locals * 40 <= len(data):
                for idx in range(num_locals):
                    v_off, v_type = struct.unpack_from("<ii", data, cur)
                    raw_name = data[cur + 8:cur + 38].rstrip(b"\0")
                    try:
                        v_name = raw_name.decode("ascii")
                        if not (v_name.isidentifier() or (v_name and all(c.isalnum() or c == '_' for c in v_name))):
                            v_name = f"local_{idx}"
                    except Exception:
                        v_name = f"local_{idx}"
                    locals_list.append(AIVariable(v_off, v_type, v_name))
                    cur += 40

        return AIFunction(key, name, stack_size, nodes, strings, locals_list)
    except Exception:
        return None


def parse_ai_model(data: bytes, key: int = 0, name: str = "") -> Optional[AIModel]:
    """Parse an AI Model (.omd / .mdl / WOW embedded) containing function & variable references.
    Supports both uncooked format (key + 4-byte extension) and cooked format (count + array of keys).
    """
    if len(data) < 8:
        return None

    model = AIModel(key, name)
    try:
        # Check uncooked format: array of (uint32 key, char[4] ext)
        count_uncooked = len(data) // 8
        is_uncooked = False
        for i in range(min(count_uncooked, 5)):
            ext = data[i * 8 + 4:i * 8 + 8].rstrip(b"\0").decode("latin-1", "replace").lower()
            if any(k in ext for k in ("ofc", "fct", "ova", "var", "fce", "fcl")):
                is_uncooked = True
                break

        if is_uncooked:
            for i in range(count_uncooked):
                ref_key = struct.unpack_from("<I", data, i * 8)[0]
                ext = data[i * 8 + 4:i * 8 + 8].rstrip(b"\0").decode("latin-1", "replace").lower()
                if not ref_key:
                    continue
                if "ofc" in ext or "fct" in ext:
                    model.function_keys.append(ref_key)
                elif "fce" in ext or "fcl" in ext:
                    model.procedure_keys.append(ref_key)
                elif "ova" in ext or "var" in ext:
                    model.var_keys.append(ref_key)
        else:
            # Cooked binary format: (uint32 zero_or_flags, uint32 count, uint32[count] keys)
            u32s = [struct.unpack_from("<I", data, i * 4)[0] for i in range(len(data) // 4)]
            if len(u32s) >= 2:
                num_entries = u32s[1]
                if 0 < num_entries <= len(u32s) - 2:
                    for k in u32s[2:2 + num_entries]:
                        if k and k != 0xFFFFFFFF:
                            model.function_keys.append(k)

        return model if (model.function_keys or model.var_keys or model.procedure_keys) else None
    except Exception:
        return None


def parse_procedure_list(data: bytes, key: int = 0) -> List[AIFunction]:
    """Parse an SCR_tt_ProcedureList (.fce / .fcl) containing named procedures and bytecode."""
    funcs = []
    if len(data) < 2:
        return funcs
    try:
        num_procs = struct.unpack_from("<H", data, 0)[0]
        pos = 2
        for p_idx in range(num_procs):
            if pos + 4 > len(data):
                break
            name_len = struct.unpack_from("<I", data, pos)[0]
            pos += 4
            proc_name = ""
            if name_len > 0 and pos + name_len <= len(data):
                proc_name = data[pos:pos + name_len].rstrip(b"\0").decode("latin-1", "replace")
                pos += name_len

            if pos + 4 > len(data):
                break
            u32_num = struct.unpack_from("<I", data, pos)[0]
            pos += 4
            stack_size = 0
            if u32_num == 0xAACCBBDD:
                if pos + 6 > len(data):
                    break
                stack_size = struct.unpack_from("<H", data, pos)[0]
                u32_num = struct.unpack_from("<I", data, pos + 2)[0]
                pos += 6

            nodes = []
            if u32_num > 0 and pos + u32_num * 8 <= len(data):
                for i in range(u32_num):
                    l_param, w_param, flags, c_type = struct.unpack_from("<ihBB", data, pos + i * 8)
                    nodes.append(AINode(i, l_param, w_param, flags, c_type))
                pos += u32_num * 8

            funcs.append(AIFunction(
                key=key,
                name=proc_name or f"Procedure_{p_idx}",
                stack_size=stack_size,
                nodes=nodes,
            ))
    except Exception:
        pass
    return funcs


def parse_ai_instance(data: bytes, key: int = 0) -> Optional[Tuple[int, int]]:
    """Parse an AI Instance (.oin) returning (model_key, vars_key)."""
    if len(data) < 8:
        return None
    try:
        model_key, vars_key = struct.unpack_from("<II", data, 0)
        return (model_key, vars_key)
    except Exception:
        return None


# ============================================================================
# 4. DISASSEMBLER (Linear Bytecode Assembly Listing)
# ============================================================================

def disassemble_ai_function(func: AIFunction) -> str:
    """Disassemble an AIFunction into a clean assembly-style listing."""
    lines = [
        f"// ============================================================================",
        f"// Function: {func.name} (Key: 0x{func.key:08X})",
        f"// Local Stack Size: {func.stack_size} bytes | Bytecode Nodes: {len(func.nodes)}",
        f"// ============================================================================",
    ]

    if func.locals:
        lines.append("// Local Variables:")
        for v in func.locals:
            lines.append(f"//   [{v.offset:04d}] {v.type_str} {v.name}")
        lines.append("")

    for node in func.nodes:
        idx_str = f"[{node.index:04d}]"
        cat = node.category_name

        if cat == "KEYWORD":
            kw = node.keyword_name
            if kw in ("JumpFalse", "JumpTrue", "Jump", "JumpFF", "JumpFalseSP", "JumpTrueSP"):
                target = node.index + node.l_param
                desc = f"KEYWORD   {kw:<12s} -> Node [{target:04d}] (offset {node.l_param:+d})"
            elif kw == "call":
                desc = f"KEYWORD   call Procedure (param={node.l_param})"
            else:
                desc = f"KEYWORD   {kw}"

        elif cat == "FUNCTION":
            fn = node.function_name
            desc = f"CALL      {fn} (ID {node.w_param})"

        elif cat == "TYPE":
            t_name = node.type_name
            if t_name == "int":
                desc = f"PUSH_INT  {node.l_param}"
            elif t_name == "float":
                desc = f"PUSH_FLT  {node.float_value:.4f}"
            elif t_name == "bool":
                desc = f"PUSH_BOOL {bool(node.l_param)}"
            elif t_name == "string":
                val = func.get_string(node.l_param)
                desc = f"PUSH_STR  \"{val}\" (offset 0x{node.l_param:X})"
            elif t_name == "object":
                desc = f"PUSH_OBJ  0x{node.l_param & 0xffffffff:08X}"
            else:
                desc = f"PUSH_{t_name.upper()} {node.l_param}"

        elif cat in ("LOCALVAR", "LOCALVARREF"):
            v_name = next((v.name for v in func.locals if v.offset == node.l_param), f"local_{node.l_param}")
            desc = f"LOCAL     {v_name} ({node.type_name}, offset {node.l_param})"

        elif cat in ("GLOBALVAR", "GLOBALVARREF"):
            desc = f"GLOBAL    var_{node.l_param} ({node.type_name}, offset {node.l_param})"

        elif cat == "FIELD":
            desc = f"FIELD     {node.field_name}"

        elif cat == "ENDTREE":
            desc = f"END_TREE"

        else:
            desc = f"{cat:<10s} w={node.w_param}, l={node.l_param}"

        lines.append(f"  {idx_str} {desc}")

    return "\n".join(lines)


# ============================================================================
# 5. HIGH-LEVEL DECOMPILER (C-Like Jade Pseudocode)
# ============================================================================

def decompile_ai_function(func: AIFunction, model_name: str = "") -> str:
    """Decompile bytecode into clean, structured, readable C-like Jade scripts."""
    if not func.nodes:
        return f"// Function {func.name} contains no executable bytecode."

    lines = [
        f"/*",
        f" * Jade Engine AI Script Decompilation",
        f" * Model: {model_name or 'Unknown_Model'}",
        f" * Function: {func.name} (Key: 0x{func.key:08X})",
        f" * Stack Size: {func.stack_size} bytes",
        f" */",
        "",
    ]

    # Declare local variables
    if func.locals:
        lines.append("// Local Variable Declarations:")
        for v in func.locals:
            lines.append(f"{v.type_str} {v.name};")
        lines.append("")

    lines.append(f"procedure {func.name}()")
    lines.append("{")

    # Stack-based AST expression evaluator and control-flow reconstructor
    expr_stack: List[str] = []
    indent = "    "
    jump_targets: Set[int] = set()

    # Pre-scan jump targets for labels
    for node in func.nodes:
        if node.c_type == 2:  # KEYWORD
            kw = node.keyword_name
            if kw in ("JumpFalse", "JumpTrue", "Jump", "JumpFF", "JumpFalseSP", "JumpTrueSP"):
                jump_targets.add(node.index + node.l_param)

    for node in func.nodes:
        if node.index in jump_targets:
            lines.append(f"label_{node.index:04d}:")

        cat = node.category_name

        if cat == "TYPE":
            t_name = node.type_name
            if t_name == "int":
                expr_stack.append(str(node.l_param))
            elif t_name == "float":
                expr_stack.append(f"{node.float_value:.3f}f")
            elif t_name == "bool":
                expr_stack.append("true" if node.l_param else "false")
            elif t_name == "string":
                s = func.get_string(node.l_param)
                expr_stack.append(f'"{s}"')
            elif t_name == "object":
                if node.l_param == 0:
                    expr_stack.append("nobody")
                else:
                    expr_stack.append(f"Object_0x{node.l_param & 0xffffffff:08X}")
            else:
                expr_stack.append(f"/* {t_name} */ {node.l_param}")

        elif cat in ("LOCALVAR", "LOCALVARREF"):
            v_name = next((v.name for v in func.locals if v.offset == node.l_param), f"local_{node.l_param}")
            expr_stack.append(v_name)

        elif cat in ("GLOBALVAR", "GLOBALVARREF"):
            expr_stack.append(f"var_{node.l_param}")

        elif cat == "FIELD":
            f_name = node.field_name
            target = expr_stack.pop() if expr_stack else "me"
            expr_stack.append(f"{target}{f_name}")

        elif cat == "FUNCTION":
            fn = node.function_name
            # Format common API calls cleanly
            args = []
            # Pop available arguments from stack
            while expr_stack:
                args.insert(0, expr_stack.pop())
                if len(args) >= 3:
                    break
            call_str = f"{fn}({', '.join(args)})"
            if not expr_stack:
                lines.append(f"{indent}{call_str};")
            else:
                expr_stack.append(call_str)

        elif cat == "KEYWORD":
            kw = node.keyword_name
            if kw in ("=", "+=", "-=", "*=", "/=", "p=", "vp="):
                val = expr_stack.pop() if expr_stack else "0"
                var = expr_stack.pop() if expr_stack else "var"
                op = "=" if "p=" in kw else kw
                lines.append(f"{indent}{var} {op} {val};")
            elif kw in ("==", "!=", ">=", "<=", ">", "<", "&&", "||", "+", "-", "*", "/", "^", "%"):
                b = expr_stack.pop() if expr_stack else "0"
                a = expr_stack.pop() if expr_stack else "0"
                expr_stack.append(f"({a} {kw} {b})")
            elif kw in ("++", "--"):
                var = expr_stack.pop() if expr_stack else "var"
                lines.append(f"{indent}{var}{kw};")
            elif kw == "!":
                a = expr_stack.pop() if expr_stack else "0"
                expr_stack.append(f"!({a})")
            elif kw == "return":
                val = expr_stack.pop() if expr_stack else ""
                lines.append(f"{indent}return {val};")
            elif kw == "stop":
                lines.append(f"{indent}stop;")
            elif kw == "returntrack":
                lines.append(f"{indent}returntrack;")
            elif kw in ("JumpFalse", "JumpFalseSP"):
                cond = expr_stack.pop() if expr_stack else "condition"
                target = node.index + node.l_param
                lines.append(f"{indent}if (!{cond}) goto label_{target:04d};")
            elif kw in ("JumpTrue", "JumpTrueSP"):
                cond = expr_stack.pop() if expr_stack else "condition"
                target = node.index + node.l_param
                lines.append(f"{indent}if ({cond}) goto label_{target:04d};")
            elif kw == "Jump":
                target = node.index + node.l_param
                lines.append(f"{indent}goto label_{target:04d};")
            elif kw == "ultra":
                # Actor modifier: (actor)@field
                actor = expr_stack.pop() if expr_stack else "me"
                expr_stack.append(f"({actor})@")
            elif kw == "call":
                lines.append(f"{indent}call_procedure();")

        elif cat == "ENDTREE":
            break

    # Flush remaining expressions
    while expr_stack:
        lines.append(f"{indent}{expr_stack.pop()};")

    lines.append("}")
    return "\n".join(lines)


# ============================================================================
# 6. BATCH BIGFILE SCRIPT EXTRACTOR
# ============================================================================

def scan_ai_scripts_from_payload(payload: bytes, source_name: str = "") -> List[Dict[str, Any]]:
    """Scan and parse all AI functions and models from a WOW/WOL raw data payload."""
    from .lzo import looks_like_pop_lzo, decompress_pop_lzo
    from .resources import parse_pop_file_entries

    if looks_like_pop_lzo(payload):
        try:
            payload = decompress_pop_lzo(payload)
        except Exception:
            pass

    results = []
    prefix = Path(source_name).stem if source_name else "Level"

    try:
        entries = parse_pop_file_entries(payload)
        for sub in entries:
            if sub.data_type == 4 and sub.size > 16:
                try:
                    sub_data = payload[sub.data_offset + 4:sub.data_offset + sub.size]
                    func = parse_ai_function(sub_data, key=sub.key, name=f"{prefix}_AI_0x{sub.key:08X}.ofc")
                    if func and func.nodes:
                        results.append({
                            "kind": "function",
                            "key": sub.key,
                            "name": f"{prefix}_AI_0x{sub.key:08X}.ofc",
                            "size": sub.size,
                            "func": func,
                            "source": source_name or "Level Payload",
                        })
                    else:
                        model = parse_ai_model(sub_data, key=sub.key, name=f"{prefix}_Model_0x{sub.key:08X}.omd")
                        if model and (model.function_keys or model.var_keys):
                            results.append({
                                "kind": "model",
                                "key": sub.key,
                                "name": f"{prefix}_Model_0x{sub.key:08X}.omd",
                                "size": sub.size,
                                "model": model,
                                "source": source_name or "Level Payload",
                            })
                except Exception:
                    continue
    except Exception:
        pass

    # If payload itself is a single standalone function or model
    if not results and len(payload) >= 16:
        try:
            f = parse_ai_function(payload, key=0, name=f"{prefix}.ofc")
            if f and f.nodes:
                results.append({
                    "kind": "function",
                    "key": 0,
                    "name": f"{prefix}.ofc",
                    "size": len(payload),
                    "func": f,
                    "source": source_name or "Standalone File",
                })
        except Exception:
            pass

    return results



def scan_all_ai_scripts_in_archive(archive) -> List[Dict[str, Any]]:
    """Scan all AI Models, Functions, Variables, and WOW embedded scripts from a BFArchive."""
    from .resources import parse_pop_file_entries

    results = []

    # 1. Standalone BigFile entries (.ofc, .fct, .omd, .mdl, .ova, .oin)
    for entry in archive.entries:
        name = (entry.name or "").lower()
        ext = name.split(".")[-1] if "." in name else ""

        if ext in ("ofc", "fct"):
            try:
                data = archive.read_entry(entry)
                func = parse_ai_function(data, key=entry.key, name=entry.name)
                if func and func.nodes:
                    results.append({
                        "kind": "function",
                        "key": entry.key,
                        "name": entry.name,
                        "size": entry.size,
                        "func": func,
                        "source": "BigFile Entry",
                    })
            except Exception:
                continue

        elif ext in ("omd", "mdl"):
            try:
                data = archive.read_entry(entry)
                model = parse_ai_model(data, key=entry.key, name=entry.name)
                if model:
                    results.append({
                        "kind": "model",
                        "key": entry.key,
                        "name": entry.name,
                        "size": entry.size,
                        "model": model,
                        "source": "BigFile Entry",
                    })
            except Exception:
                continue

        # 2. Embedded WOW Room / Character asset type 4 (scripts)
        elif "wow" in name:
            try:
                data = archive.read_entry(entry)
                for sub in parse_pop_file_entries(data):
                    if sub.data_type == 4 and sub.size > 16:
                        sub_data = data[sub.data_offset + 4:sub.data_offset + sub.size]
                        # Try parsing as function
                        func = parse_ai_function(sub_data, key=sub.key, name=f"WOW_AI_0x{sub.key:08X}")
                        if func and func.nodes:
                            results.append({
                                "kind": "function",
                                "key": sub.key,
                                "name": f"{entry.name}_0x{sub.key:08X}.ofc",
                                "size": sub.size,
                                "func": func,
                                "source": f"Embedded in {entry.name}",
                            })
                        else:
                            # Try parsing as model
                            model = parse_ai_model(sub_data, key=sub.key, name=f"{entry.name}_Model_0x{sub.key:08X}")
                            if model and (model.function_keys or model.var_keys):
                                results.append({
                                    "kind": "model",
                                    "key": sub.key,
                                    "name": f"{entry.name}_0x{sub.key:08X}.omd",
                                    "size": sub.size,
                                    "model": model,
                                    "source": f"Embedded in {entry.name}",
                                })
            except Exception:
                continue

    return results


def export_decompiled_scripts_to_dir(scripts: List[Dict[str, Any]], output_dir: str | Path) -> int:
    """Export all decompiled AI scripts to .jade and .asm files in output_dir."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    count = 0

    for item in scripts:
        if item["kind"] == "function":
            func: AIFunction = item["func"]
            decompiled = decompile_ai_function(func)
            disassembled = disassemble_ai_function(func)

            base_name = re.sub(r'[\\/*?:"<>|]', "_", item["name"])
            script_path = out / f"{base_name}.jade"
            asm_path = out / f"{base_name}.asm"

            script_path.write_text(decompiled, encoding="utf-8")
            asm_path.write_text(disassembled, encoding="utf-8")
            count += 1

        elif item["kind"] == "model":
            model: AIModel = item["model"]
            lines = [
                f"// Jade AI Model: {model.name} (Key: 0x{model.key:08X})",
                f"// Referenced Functions: {len(model.function_keys)}",
                f"// Referenced Variables: {len(model.var_keys)}",
                "",
                "model {",
            ]
            for fk in model.function_keys:
                lines.append(f"    function 0x{fk:08X};")
            for vk in model.var_keys:
                lines.append(f"    variable 0x{vk:08X};")
            lines.append("}\n")

            base_name = re.sub(r'[\\/*?:"<>|]', "_", item["name"])
            model_path = out / f"{base_name}.jade"
            model_path.write_text("\n".join(lines), encoding="utf-8")
            count += 1

    return count

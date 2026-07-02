#!/usr/bin/env python3
import re, sys, os, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
# docs/keymap/ -> repo root is two levels up
SRC = os.path.join(HERE, "..", "..", "miryoku", "custom_config.h")
txt = open(SRC).read()

LAYERS = ["BASE","NAV","MOUSE","MEDIA","NUM","SYM","FUN"]

def grab(name):
    # capture the #define MIRYOKU_LAYER_<name> ... block (line-continued)
    m = re.search(r"#define\s+MIRYOKU_LAYER_"+name+r"\b(.*?)(?=\n#define|\Z)", txt, re.S)
    body = m.group(1)
    # join continuation lines
    body = body.replace("\\\n"," ").replace("\\"," ")
    body = body.strip()
    return body

def split_top(body):
    # paren-aware comma split
    out=[]; depth=0; cur=""
    for ch in body:
        if ch=='(': depth+=1; cur+=ch
        elif ch==')': depth-=1; cur+=ch
        elif ch==',' and depth==0:
            out.append(cur.strip()); cur=""
        else: cur+=ch
    if cur.strip(): out.append(cur.strip())
    return out

# label mapping
LAYNAME={"U_MEDIA":"Media","U_NAV":"Nav","U_MOUSE":"Mouse","U_SYM":"Sym",
         "U_NUM":"Num","U_FUN":"Fun","U_BUTTON":"Btn","U_BASE":"Base"}
MODNAME={"LGUI":"GUI","RGUI":"GUI","LALT":"ALT","RALT":"AltGr","LCTRL":"CTRL",
         "RCTRL":"CTRL","LSHFT":"SHFT","RSHFT":"SHFT"}
SPECIAL={
 "U_NP":"", "U_NA":"", "U_NU":"", "U_BOOT":"BOOT",
 "U_RDO":"Redo","U_PST":"Paste","U_CPY":"Copy","U_CUT":"Cut","U_UND":"Undo",
 "U_MS_L":{"t":"Ms","h":"←"},"U_MS_R":{"t":"Ms","h":"→"},
 "U_MS_U":{"t":"Ms","h":"↑"},"U_MS_D":{"t":"Ms","h":"↓"},
 "U_WH_L":{"t":"Whl","h":"←"},"U_WH_R":{"t":"Whl","h":"→"},
 "U_WH_U":{"t":"Whl","h":"↑"},"U_WH_D":{"t":"Whl","h":"↓"},
 "U_BTN1":"LClk","U_BTN2":"RClk","U_BTN3":"MClk",
}
KC={"LEFT":"←","RIGHT":"→","UP":"↑","DOWN":"↓","BSPC":"Bspc","DEL":"Del",
 "RET":"Enter","SPACE":"Spc","TAB":"Tab","ESC":"Esc","INS":"Ins",
 "HOME":"Home","END":"End","PG_UP":"PgUp","PG_DN":"PgDn","GRAVE":"`","SQT":"'",
 "SEMI":";","COMMA":",","DOT":".","SLASH":"/","BSLH":"\\","EQUAL":"=","MINUS":"-",
 "LBKT":"[","RBKT":"]","LBRC":"{","RBRC":"}","LPAR":"(","RPAR":")","UNDER":"_",
 "PLUS":"+","PIPE":"|","TILDE":"~","EXCL":"!","AT":"@","HASH":"#","DLLR":"$",
 "PRCNT":"%","CARET":"^","AMPS":"&","ASTRK":"*","COLON":":",
 "C_PREV":"⏮","C_NEXT":"⏭","C_VOL_DN":"Vol-","C_VOL_UP":"Vol+","C_MUTE":"Mute",
 "C_PP":"⏯","C_STOP":"⏹","K_APP":"Menu","PSCRN":"PrtSc","SLCK":"ScrLk",
 "PAUSE_BREAK":"Pause","CAPS":"Caps",
}
def kc(x):
    x=x.strip()
    return KC.get(x, x)

def label(tok):
    tok=tok.strip()
    if tok in SPECIAL: return SPECIAL[tok]
    if tok.startswith("U_MT("):
        mod,key = split_top(tok[5:-1])
        return {"t":kc(key),"h":MODNAME.get(mod.strip(),mod.strip())}
    if tok.startswith("U_LT("):
        lay,key = split_top(tok[5:-1])
        return {"t":kc(key),"h":LAYNAME.get(lay.strip(),lay.strip())}
    if tok.startswith("&kp "):
        return kc(tok[4:])
    if tok.startswith("&u_to_"):
        return "→"+LAYNAME.get(tok.replace("&u_to_",""), tok.replace("&u_to_U_",""))
    if tok=="&u_caps_word": return "CapsWd"
    if tok.startswith("&u_bt_sel_"): return "BT"+tok[-1]
    if tok=="&u_out_tog": return "OutTog"
    if tok.startswith("&studio_unlock"): return "Studio"
    return tok

layers_out={}
for L in LAYERS:
    toks=split_top(grab(L))
    assert len(toks)==40, f"{L}: got {len(toks)}"
    # physical order matching totem_info.json:
    # row0(0:10) row1(10:20) row2[ K38 , K20..K29 , K39 ] thumbs(K32..K37 = 32:38)
    order = toks[0:10] + toks[10:20] + [toks[38]] + toks[20:30] + [toks[39]] + toks[32:38]
    assert len(order)==38, f"{L}: order {len(order)}"
    layers_out["Base" if L=="BASE" else LAYNAME[f"U_{L}"]] = [label(t) for t in order]

doc={
 "layout":{"qmk_info_json": os.path.join(HERE,"totem_info.json"), "layout_name":"LAYOUT"},
 "layers":layers_out,
}
open("totem.yaml","w").write(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False))
print("OK layers:", list(layers_out))

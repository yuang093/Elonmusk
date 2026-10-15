# EXPANDED 44-entry KNOWN_CLEARED_BYLINE_IDS set (cycle 1017 1st-fire EXPANSION 42 -> 44 entries)

## Set expansion history (forward-extension lineage)

| Cycle | Expansion | New entries | Set size |
|---|---|---|---|
| cycle 968 | canonical 23-entry base (cycle 909/911/915/918/919/920/925/926/931/932/946/954/964/963 cleared entries) | (base) | 23 |
| cycle 974 | EXPANSION #1: +2 cycle 973 NEW bare-byline IDs (2110123414476493004 + 2110125596424516006) | 2 | 25 |
| cycle 976 | EXPANSION #2: +1 cycle 975 NEW bare-byline ID (2110154589278503175) | 1 | 26 |
| cycle 981 | EXPANSION #3: +4 cycle 980 NEW bare-byline IDs (2110187662124749238 + 2110220345420771699 + 2110220573418885246 + 2110221961997713444) | 4 | 30 |
| cycle 990 | EXPANSION #4: +2 cycle 989 NEW bare-byline IDs (2110225499205390759 + 2110364181996433785) | 2 | 32 |
| cycle 991 | EXPANSION #5: +2 cycle 991 NEW bare-byline IDs (2110393133498528170 + 2110393370262839718) | 2 | 32 (set STAYS at 32 because 991 had pre-clear but no expansion; cycle 991 commits the EXPANDED 32 set) |
| cycle 993 | EXPANSION #6: +1 cycle 992 NEW bare-byline ID (2110402790958977065) | 1 | 33 |
| cycle 994 | EXPANSION #7: +1 cycle 994 NEW bare-byline ID (2110407463384318196) | 1 | 34 |
| cycle 999 | EXPANSION #8: +2 cycle 999 NEW bare-byline IDs (2110480720301081080 + 2110516939873517989) | 2 | 36 |
| cycle 1001 | EXPANSION #9: +3 cycle 1001 NEW bare-byline IDs (2110544339701039179 + 2110549391211679822 + 2110567340069003542) | 3 | 39 |
| cycle 1005 | EXPANSION #10: +1 cycle 1005 NEW bare-byline ID (2110613300421542383) | 1 | 40 |
| cycle 1011 | EXPANSION #11: +1 cycle 1011 NEW bare-byline ID (2110618291399962816) | 1 | 41 |
| cycle 1016 | EXPANSION #12: +1 cycle 1016 NEW bare-byline ID (2110706336812155334) | 1 | 42 |
| **cycle 1017** | **EXPANSION #13: +2 cycle 1017 NEW bare-byline IDs (2110784494076657699 + 2110787996848980191)** | **2** | **44** |

## Full 44-entry set (cycle 1017 EXPANDED, committed at SHA TBD→4a769dc)

```python
KNOWN_CLEARED_BYLINE_IDS = {
    # 2 records cleared at cycles 909/911/915/918 (Phase 0.5 byline-revert 1st/2nd/3rd/4th-fire)
    "2109035557003415838",
    "2109072353351348430",
    # 3 records cleared at cycle 919 (Phase 0.5b byline-only NEW-record pre-clear 1st-fire SUBSTANTIVE)
    "2109259882901672249",
    "2109261306070970507",
    "2109262249970028683",
    # 3 records cleared at cycle 920 (Phase 0.5b byline-only NEW-record pre-clear 2nd-fire SUBSTANTIVE)
    "2109267925375045958",
    "2109269988947480736",
    "2109274577562198241",
    # 1 record cleared at cycle 925 (Phase 0.5b byline-only NEW-record pre-clear 3rd-fire SUBSTANTIVE)
    "2109274704959930775",
    # 2 records cleared at cycle 926 (Phase 0.5b byline-only NEW-record pre-clear 4th-fire SUBSTANTIVE)
    "2109349314912764171",
    "2109367117334323515",
    # 1 record cleared at cycle 931 (Phase 0.5b byline-only NEW-record pre-clear 6th-fire SUBSTANTIVE)
    "2109459464617402794",
    # 2 records cleared at cycle 932 (Phase 0.5b byline-only NEW-record pre-clear 7th-fire SUBSTANTIVE)
    "2109469889236804058",
    "2109471223642218746",
    # 2 records cleared at cycle 946 (Phase 0.5b byline-only NEW-record pre-clear 9th-fire SUBSTANTIVE)
    "2109688396520276469",
    "2109688880853119009",
    # 1 record cleared at cycle 954 (Phase 0.5b byline-only NEW-record pre-clear 9th-fire SUBSTANTIVE)
    "2109793718362390945",
    # 2 records cleared at cycle 964 (Phase 0.5b byline-only NEW-record pre-clear 11th-fire SUBSTANTIVE)
    "2109954931721650623",
    "2109969797312356746",
    # 2 records cleared at cycle 963 (Phase 0.5b byline-only NEW-record pre-clear 10th-fire SUBSTANTIVE)
    "2109860799347085804",
    "2109867408236351855",
    # 2 records cleared at cycle 973 (Phase 0.5b byline-only NEW-record pre-clear 13th-fire SUBSTANTIVE)
    "2110123414476493004",
    "2110125596424516006",
    # 1 record cleared at cycle 975 (Phase 0.5b byline-only NEW-record pre-clear 14th-fire SUBSTANTIVE)
    "2110154589278503175",
    # 4 records cleared at cycle 980 (Phase 0.5b byline-only NEW-record pre-clear 15th-fire SUBSTANTIVE)
    "2110187662124749238",
    "2110220345420771699",
    "2110220573418885246",
    "2110221961997713444",
    # 2 records cleared at cycle 989 (Phase 0.5b byline-only NEW-record pre-clear 16th-fire SUBSTANTIVE)
    "2110225499205390759",
    "2110364181996433785",
    # 2 records cleared at cycle 991 (Phase 0.5b byline-only NEW-record pre-clear 17th-fire SUBSTANTIVE)
    "2110393133498528170",
    "2110393370262839718",
    # 1 record cleared at cycle 992 (Phase 0.5b byline-only NEW-record pre-clear 18th-fire SUBSTANTIVE)
    "2110402790958977065",
    # 1 record cleared at cycle 994 (Phase 0.5b byline-only NEW-record pre-clear 19th-fire SUBSTANTIVE)
    "2110407463384318196",
    # 2 records cleared at cycle 999 (Phase 0.5b byline-only NEW-record pre-clear 20th-fire SUBSTANTIVE)
    "2110480720301081080",
    "2110516939873517989",
    # 3 records cleared at cycle 1001 (Phase 0.5b byline-only NEW-record pre-clear 22nd-fire SUBSTANTIVE)
    "2110544339701039179",
    "2110549391211679822",
    "2110567340069003542",
    # 1 record cleared at cycle 1005 (Phase 0.5b byline-only NEW-record pre-clear 24th-fire SUBSTANTIVE)
    "2110613300421542383",
    # 1 record cleared at cycle 1011 (Phase 0.5b byline-only NEW-record pre-clear 25th-fire SUBSTANTIVE)
    "2110618291399962816",
    # 1 record cleared at cycle 1016 (Phase 0.5b byline-only NEW-record pre-clear 26th-fire SUBSTANTIVE)
    "2110706336812155334",
    # 2 records cleared at cycle 1017 (Phase 0.5b byline-only NEW-record pre-clear 27th-fire SUBSTANTIVE)
    "2110784494076657699",
    "2110787996848980191",
}
```

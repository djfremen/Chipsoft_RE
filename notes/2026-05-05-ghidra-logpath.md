# Ghidra log-path resolution + JSON open site

Function containing 0x10011aa4: FUN_10011a99 @ 0x10011a99

## Functions near 0x10011aa4

- FUN_100101b0 @ 0x100101b0
- FUN_10010250 @ 0x10010250
- FUN_10010280 @ 0x10010280
- FUN_10010550 @ 0x10010550
- Catch_All@100119e9 @ 0x100119e9
- FUN_10011a99 @ 0x10011a99
- FUN_10011cd0 @ 0x10011cd0
- FUN_10012100 @ 0x10012100
- FUN_10012890 @ 0x10012890
- FUN_10012950 @ 0x10012950
- FUN_10012980 @ 0x10012980
- FUN_10012f20 @ 0x10012f20
- FUN_10012f80 @ 0x10012f80
- FUN_10012f90 @ 0x10012f90

### FUN_10011a99 @ 0x10011a99

**Strings referenced (max 40):**
- 0x10011aa3 → 0x100e0bec  `\logs\`
- 0x10011ac0 → 0x100e0bd8  `%Y%m%d_%H%M%S.log`
- 0x10011aff → 0x100e0bbc  `[%TimeStamp%]: %Message%`
- 0x10011b41 → 0x100e0858  `Severity`

```c

void FUN_10011a99(void)

{
  byte bVar1;
  undefined4 *puVar2;
  uint *puVar3;
  undefined4 uVar4;
  int *piVar5;
  void *pvVar6;
  int *piVar7;
  uint unaff_EBP;
  int unaff_EDI;
  undefined4 uStack0000000c;
  undefined1 uVar8;
  
  if (*(byte *)(unaff_EDI + 0xc) < 5) {
    *(undefined1 *)(unaff_EBP - 0x2c1) = 1;
    puVar2 = FUN_1000b740((undefined4 *)(unaff_EBP - 0x2dc),(uint *)(unaff_EBP - 0x238),
                          (uint *)"\\logs\\");
    *(undefined1 *)(unaff_EBP - 4) = 0x43;
    puVar3 = FUN_1000b830((uint *)(unaff_EBP - 0x250),puVar2,(uint *)"%Y%m%d_%H%M%S.log");
    *(undefined1 *)(unaff_EBP - 4) = 0x44;
    *(uint **)(unaff_EBP - 0x318) = puVar3;
    *(uint *)(unaff_EBP - 0x2e0) = unaff_EBP - 0x2c1;
    *(char **)(unaff_EBP - 0x220) = "[%TimeStamp%]: %Message%";
    FUN_100213e0((int *)(unaff_EBP - 0x2e8),(undefined4 *)(unaff_EBP - 0x318),
                 (undefined4 *)(unaff_EBP - 0x220),(undefined4 *)(unaff_EBP - 0x2e0));
    FUN_1000e120((int *)(unaff_EBP - 0x2e4));
    FUN_10002f70((int *)(unaff_EBP - 0x250));
    *(undefined1 *)(unaff_EBP - 4) = 0x23;
    FUN_10002f70((int *)(unaff_EBP - 0x2dc));
    bVar1 = *(byte *)(unaff_EDI + 0xc);
    uVar4 = FUN_1006b4b0((PSRWLOCK)"Severity");
    *(undefined4 *)(unaff_EBP - 800) = uVar4;
    *(uint *)(unaff_EBP - 0x318) = (uint)bVar1;
    FUN_10021420((void *)(unaff_EBP - 0x220),(undefined4 *)(unaff_EBP - 800));
    *(undefined1 *)(unaff_EBP - 4) = 0x45;
    piVar5 = FUN_1006cd40((undefined4 *)(unaff_EBP - 0x2e8));
    piVar7 = (int *)(unaff_EBP - 0x220);
    *(undefined1 *)(unaff_EBP - 4) = 0x46;
    pvVar6 = (void *)FUN_1001d870(piVar5);
    FUN_1006d550(pvVar6,piVar7);
    FUN_1000e120((int *)(unaff_EBP - 0x2e4));
    *(undefined1 *)(unaff_EBP - 4) = 0x23;
    FUN_1001f060((int *)(unaff_EBP - 0x220));
    FUN_1000f610();
    piVar7 = FUN_1006cd40((undefined4 *)(unaff_EBP - 0x2e8));
    uVar8 = 1;
    *(undefined1 *)(unaff_EBP - 4) = 0x47;
    pvVar6 = (void *)FUN_1001d870(piVar7);
    FUN_1006d5e0(pvVar6,uVar8);
    *(undefined1 *)(unaff_EBP - 4) = 0x23;
    FUN_1000e120((int *)(unaff_EBP - 0x2e4));
  }
  *(int *)(unaff_EBP - 0x318) = unaff_EDI;
  puVar2 = (undefined4 *)FUN_10021470((void *)(unaff_EBP - 0x2e8),(undefined4 *)(unaff_EBP - 0x318))
  ;
  FUN_1000ce40((void *)(unaff_EDI + 0x260),puVar2);
  if (*(int *)(unaff_EBP - 0x2e4) == 0) {
    FUN_10002f70((int *)(unaff_EBP - 0x238));
    FUN_10020bc0((int *)(unaff_EBP - 0x290));
    FUN_10002f70((int *)(unaff_EBP - 0x2a8));
    FUN_1000f490((int *)(unaff_EBP - 0x2c0));
    ExceptionList = *(void **)(unaff_EBP - 0xc);
    uStack0000000c = 0x10011c60;
    __security_check_cookie(*(uint *)(unaff_EBP - 0x14) ^ unaff_EBP);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_100a04e8();
}


```

## Search: refs to 'options.json' literal address (0x100e0714)

- 0x10001ac2 ← (no function)
- 0x10001772 ← (no function)
- 0x100013f2 ← (no function)

## .data slots holding 'options.json' pointer (raw scan)


## Functions referencing the std::string slots holding 'options.json'


## Decompiles of options.json-referencing functions


# Ghidra transport-layer — j2534_interface.dll

Round 3: between framers and Win32 serial APIs.

## .rdata strings near suspected path-format references

- 0x100e50a0  `\\.\`
- 0x100e5000  `IOCTL_CMD (`
- 0x100e5020  `_event`
- 0x100e5040  `ad`
- 0x100e5060  `elIoEx`
- 0x100e5080  `nvert calendar time to UTC time`

## write_transport (called by write_framer FUN_100321a0) — 0x1001a140

**Strings referenced:**
- 0x1001a34d → 0x100e10a0  `Add async message to queue`
- 0x1001a364 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001a369 → 0x100e1330  `m_pStreamCompound != 0`
- 0x1001a4cb → 0x100e10a0  `Add async message to queue`

**Outgoing calls (unique):**
- 0x10055040  __alloca_probe
- 0x10040faa  __Mtx_lock
- 0x1004087b  _Throw_C_error
- 0x100942c0  _memset
- 0x10093750  FUN_10093750
- 0x1001f210  FUN_1001f210
- 0x10053c4a  FUN_10053c4a
- 0x1001de30  FUN_1001de30
- 0x1004021f  __Cnd_signal
- 0x1005f320  FUN_1005f320
- 0x10020d90  FUN_10020d90
- 0x10007bd0  FUN_10007bd0
- 0x100573c0  FUN_100573c0
- 0x1005cd00  ___uncaught_exceptions
- 0x1000b420  FUN_1000b420
- 0x100a600c  FID_conflict:__assert
- 0x10007b10  FUN_10007b10
- 0x10031fd0  FUN_10031fd0
- 0x10031d60  FUN_10031d60
- 0x10053fdd  FUN_10053fdd
- 0x1000c2f0  FUN_1000c2f0
- 0x1001d730  FUN_1001d730
- 0x10004940  FUN_10004940
- 0x1006cb90  FUN_1006cb90
- 0x1001d270  FUN_1001d270
- 0x10040fcf  __Mtx_unlock
- 0x100a0858  _clock
- 0x10018510  FUN_10018510
- 0x10017840  FUN_10017840
- 0x10053c39  __security_check_cookie
- 0x1009cac3  FUN_1009cac3

```c

/* WARNING: Function: __alloca_probe replaced with injection: alloca_probe */
/* WARNING: Removing unreachable block (ram,0x1001a48b) */

void FUN_1001a140(undefined *param_1,uint *param_2,void **param_3)

{
  void *this;
  undefined1 uVar1;
  wchar_t *pwVar2;
  int iVar3;
  void *this_00;
  undefined4 *puVar4;
  clock_t cVar5;
  clock_t cVar6;
  uint uVar7;
  byte ****ppppbVar8;
  undefined4 ****ppppuVar9;
  uint uVar10;
  uint unaff_EDI;
  undefined4 *puVar11;
  undefined4 uVar12;
  int *piVar13;
  undefined4 **ppuVar14;
  char *pcVar15;
  wchar_t *pwVar16;
  undefined *local_10a8;
  uint local_10a4;
  undefined4 local_10a0;
  undefined4 local_109c;
  undefined2 local_1098;
  undefined4 local_1096;
  undefined1 local_1092 [3954];
  int local_120 [4];
  int local_110 [41];
  int local_6c;
  undefined4 *local_68;
  undefined4 local_64;
  undefined4 ***local_60 [4];
  uint local_50;
  uint local_4c;
  undefined4 local_48;
  undefined4 *local_44;
  void **local_40;
  byte ***local_3c [4];
  int local_2c;
  uint local_28;
  undefined8 local_24;
  int local_1c;
  undefined4 ***local_18;
  undefined4 uStack_14;
  void *local_10;
  undefined1 *puStack_c;
  uint local_8;
  
  this = DAT_10104d5c;
  local_8 = 0xffffffff;
  puStack_c = &LAB_100c31f3;
  local_10 = ExceptionList;
  uStack_14 = 0x1001a15b;
  pwVar2 = (wchar_t *)(DAT_100fc0f4 ^ (uint)&stack0xfffffffc);
  ExceptionList = &local_10;
  local_40 = param_3;
  local_18 = (undefined4 ***)pwVar2;
  if (*param_2 == 0) {
    local_24 = ZEXT48((_Mtx_internal_imp_t *)((int)DAT_10104d5c + 0xb0));
    iVar3 = __Mtx_lock((_Mtx_internal_imp_t *)((int)DAT_10104d5c + 0xb0));
    if (iVar3 != 0) {
      std::_Throw_C_error(iVar3);
    }
    local_24._0_5_ = CONCAT14(1,(int)local_24);
    local_8._0_1_ = 0;
    local_8._1_3_ = 0;
    local_1098 = 0;
    local_1096 = 0;
    local_10a0 = 0;
    local_109c = 0;
    _memset(local_1092,0,0x1022);
    local_10a8 = param_1;
    FUN_10093750(&local_10a4,param_2,0x1034);
    uVar7 = *(uint *)((int)this + 0x168);
    if (uVar7 <= *(int *)((int)this + 0x170) + 1U) {
      FUN_1001f210((int)this + 0x160);
      uVar7 = *(uint *)((int)this + 0x168);
    }
    *(uint *)((int)this + 0x16c) = *(uint *)((int)this + 0x16c) & uVar7 - 1;
    iVar3 = *(int *)((int)this + 0x164);
    local_1c = (*(int *)((int)this + 0x168) - 1U &
               *(int *)((int)this + 0x170) + *(int *)((int)this + 0x16c)) * 4;
    if (*(int *)(local_1c + iVar3) == 0) {
      iVar3 = FUN_10053c4a(0x105b);
      uVar1 = (undefined1)local_8;
      if (iVar3 == 0) {
LAB_1001a533:
        local_8._0_1_ = uVar1;
                    /* WARNING: Subroutine does not return */
        local_10a8 = &UNK_1001a538;
        FUN_1009cac3();
      }
      uVar7 = iVar3 + 0x23U & 0xffffffe0;
      *(int *)(uVar7 - 4) = iVar3;
      *(uint *)(local_1c + *(int *)((int)this + 0x164)) = uVar7;
      iVar3 = *(int *)((int)this + 0x164);
    }
    puVar11 = (undefined4 *)0x1001a292;
    FUN_10093750(*(uint **)(local_1c + iVar3),(uint *)&local_10a8,0x1038);
    *(int *)((int)this + 0x170) = *(int *)((int)this + 0x170) + 1;
    *(undefined1 *)((int)this + 0x174) = 1;
    FUN_1001de30((int *)&local_24);
    local_8 = CONCAT31(local_8._1_3_,1);
    iVar3 = __Cnd_signal((int *)((int)this + 0x110));
    if (iVar3 != 0) {
      std::_Throw_C_error(iVar3);
    }
    local_8 = local_8 & 0xffffff00;
    if (*(byte *)((int)this + 0xc) < 5) {
      local_44 = &local_48;
      local_1c = 0;
      ppuVar14 = &local_44;
      piVar13 = &local_1c;
      local_48 = 1;
      this_00 = (void *)FUN_1005f320();
      FUN_10020d90(this_00,piVar13,ppuVar14);
      local_8._0_1_ = 2;
      while (local_1c != 0) {
        FUN_10007bd0(local_120);
        local_8._0_1_ = 3;
        local_6c = FUN_1005f320();
        puVar4 = FUN_100573c0(&local_1c);
        local_68 = puVar4;
        local_64 = ___uncaught_exceptions();
        piVar13 = local_110;
        local_8 = CONCAT31(local_8._1_3_,4);
        pcVar15 = "Add async message to queue";
        uVar12 = 0x1001a358;
        FUN_1000b420(piVar13,"Add async message to queue");
        if (puVar4 == (undefined4 *)0x0) {
          unaff_EDI = 0x216;
          pwVar2 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
          pwVar16 = L"m_pStreamCompound != 0";
          piVar13 = (int *)0x1001a373;
          FID_conflict___assert
                    (L"m_pStreamCompound != 0",
                     L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216
                    );
          pcVar15 = (char *)pwVar16;
        }
        FUN_10007b10(local_120,&stack0xffffef38);
        FUN_10031fd0(local_3c,puVar11,uVar12,piVar13,pcVar15,(uint)pwVar2,unaff_EDI);
        local_8._0_1_ = 5;
        ppppbVar8 = local_3c;
        if (0xf < local_28) {
          ppppbVar8 = (byte ****)local_3c[0];
        }
        FUN_10031d60(local_60,(byte *)ppppbVar8,local_2c);
        local_8._0_1_ = 4;
        uVar1 = (undefined1)local_8;
        local_8._0_1_ = 4;
        if (0xf < local_28) {
          ppppbVar8 = (byte ****)local_3c[0];
          if ((0xfff < local_28 + 1) &&
             (ppppbVar8 = (byte ****)local_3c[0][-1],
             (byte *)0x1f < (byte *)((int)local_3c[0] + (-4 - (int)ppppbVar8)))) goto LAB_1001a533;
          FUN_10053fdd(ppppbVar8);
        }
        local_2c = 0;
        local_28 = 0xf;
        local_3c[0] = (byte ***)((uint)local_3c[0] & 0xffffff00);
        local_8._0_1_ = 6;
        pwVar2 = (wchar_t *)local_60;
        if (0xf < local_4c) {
          pwVar2 = (wchar_t *)local_60[0];
        }
        unaff_EDI = local_50;
        FUN_1000c2f0(puVar4 + 0x18,pwVar2,local_50);
        local_8._0_1_ = 4;
        if (0xf < local_4c) {
          local_10a8 = (undefined *)(local_4c + 1);
          ppppuVar9 = (undefined4 ****)local_60[0];
          if ((undefined *)0xfff < local_10a8) {
            ppppuVar9 = (undefined4 ****)local_60[0][-1];
            local_10a8 = (undefined *)(local_4c + 0x24);
            uVar1 = (undefined1)local_8;
            if (0x1f < (uint)((int)local_60[0] + (-4 - (int)ppppuVar9))) goto LAB_1001a533;
          }
          FUN_10053fdd(ppppuVar9);
        }
        local_50 = 0;
        local_4c = 0xf;
        local_60[0] = (undefined4 ***)((uint)local_60[0] & 0xffffff00);
        local_8._0_1_ = 3;
        local_10a8 = (undefined *)0x1001a469;
        FUN_1001d730(&local_6c);
        local_8._0_1_ = 2;
        local_10a8 = (undefined *)0x1001a478;
        FUN_10004940(local_120);
      }
      local_8 = (uint)local_8._1_3_ << 8;
      local_1c = 0;
    }
    FUN_1001d270(this,0x22,param_2,(short)param_2[3] + 0x14,(uint *)local_40,*param_2 + 3000);
    local_8 = 7;
    if (local_24._4_1_ != '\0') {
      iVar3 = __Mtx_unlock((int)local_24);
      if (iVar3 != 0) {
        std::_Throw_C_error(iVar3);
      }
    }
  }
  else {
    cVar5 = _clock();
    FUN_10018510((int)this);
    cVar6 = _clock();
    uVar10 = (*param_2 - cVar6) + cVar5;
    uVar7 = 0;
    if (-1 < (int)uVar10) {
      uVar7 = uVar10;
    }
    *param_2 = uVar7;
    FUN_10017840(this,(int)param_1,param_2,local_40);
  }
  ExceptionList = local_10;
  __security_check_cookie((uint)local_18 ^ (uint)&stack0xfffffffc);
  return;
}


```

## read_transport  (called by read_framer  FUN_1001a540) — 0x10016e10

**Strings referenced:**
- 0x10016f71 → 0x100e0f08  `Messages in queue: `
- 0x10016fb3 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x10016fb8 → 0x100e1330  `m_pStreamCompound != 0`
- 0x10017415 → 0x100e0f1c  `Error in message: `
- 0x1001745c → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x10017461 → 0x100e1330  `m_pStreamCompound != 0`
- 0x10017582 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x10017587 → 0x100e1534  `m_record != 0`
- 0x100175ad → 0x100e1360  `e:\libs\boost\boost_1_65_1\boost\smart_ptr\shared_ptr.hpp`
- 0x100175b2 → 0x100e13d4  `px != 0`

**Outgoing calls (unique):**
- 0x10055040  __alloca_probe
- 0x100a0858  _clock
- 0x10018510  FUN_10018510
- 0x1005f320  FUN_1005f320
- 0x10020d90  FUN_10020d90
- 0x10007bd0  FUN_10007bd0
- 0x100573c0  FUN_100573c0
- 0x1005cd00  ___uncaught_exceptions
- 0x1000b420  FUN_1000b420
- 0x1001e920  FUN_1001e920
- 0x100a600c  FID_conflict:__assert
- 0x10007b10  FUN_10007b10
- 0x10031fd0  FUN_10031fd0
- 0x10031d60  FUN_10031d60
- 0x10053fdd  FUN_10053fdd
- 0x1000c2f0  FUN_1000c2f0
- 0x1001d730  FUN_1001d730
- 0x10004940  FUN_10004940
- 0x1006cb90  FUN_1006cb90
- 0x10053c4a  FUN_10053c4a
- 0x100942c0  _memset
- 0x10031660  FUN_10031660
- 0x10021980  FUN_10021980
- 0x100410e4  __Xtime_get_ticks
- 0x10021680  FUN_10021680
- 0x100216c0  FUN_100216c0
- 0x1001d270  FUN_1001d270
- 0x10021700  FUN_10021700
- 0x10021650  FUN_10021650
- 0x10036160  FUN_10036160
- 0x1000a810  FUN_1000a810
- 0x1006d0d0  FUN_1006d0d0
- 0x10057df0  FUN_10057df0
- 0x10016d40  FUN_10016d40
- 0x10037e90  FUN_10037e90
- 0x10053c39  __security_check_cookie
- 0x1009cac3  FUN_1009cac3

```c

/* WARNING: Function: __alloca_probe replaced with injection: alloca_probe */
/* WARNING: Removing unreachable block (ram,0x100172a2) */
/* WARNING: Removing unreachable block (ram,0x10017269) */
/* WARNING: Removing unreachable block (ram,0x100172ee) */
/* WARNING: Removing unreachable block (ram,0x100170d2) */
/* WARNING: Removing unreachable block (ram,0x10017605) */
/* WARNING: Type propagation algorithm not settling */

void __thiscall
FUN_10016e10(void *this,undefined4 *param_1,int param_2,int *param_3,undefined4 **param_4)

{
  char cVar1;
  ushort uVar2;
  longlong lVar3;
  undefined1 uVar4;
  clock_t cVar5;
  clock_t cVar6;
  undefined4 *puVar7;
  undefined4 *puVar8;
  void *pvVar9;
  undefined4 *puVar10;
  byte *******pppppppbVar11;
  int iVar12;
  undefined8 *puVar13;
  uint *puVar14;
  uint *puVar15;
  undefined4 *******pppppppuVar16;
  undefined4 *puVar17;
  uint uVar18;
  int *piVar19;
  undefined4 **ppuVar20;
  uint uVar21;
  longlong lVar22;
  undefined4 *puVar23;
  void **ppvVar24;
  char *pcVar25;
  undefined4 ***pppuVar26;
  wchar_t *pwVar27;
  wchar_t *pwVar28;
  undefined4 **ppuVar29;
  uint local_316c [4];
  int local_315c [5];
  uint local_3148 [35];
  undefined4 *******local_30bc [4];
  uint local_30ac;
  uint local_30a8;
  int local_30a4;
  undefined8 local_30a0;
  int *local_3094;
  int *local_3090;
  uint local_308c;
  undefined4 **local_3088;
  undefined4 *local_3084;
  undefined4 *local_3080;
  undefined8 local_307c;
  undefined4 *local_3074;
  uint local_3070;
  undefined4 *local_306c;
  ushort local_3066;
  uint local_3064;
  int local_3060 [3];
  ushort auStack_3052 [6137];
  byte *******local_60 [3];
  int local_54;
  undefined4 *local_50;
  uint local_4c;
  byte *******local_48 [4];
  uint local_38;
  uint local_34;
  int local_30;
  undefined4 *local_2c;
  undefined4 *local_28;
  void *local_24;
  uint local_20;
  undefined4 *local_1c;
  void *local_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_100c2db1;
  local_10 = ExceptionList;
  local_14 = DAT_100fc0f4 ^ (uint)&stack0xfffffffc;
  ExceptionList = &local_10;
  local_3090 = param_3;
  local_3070 = 0;
  local_306c = this;
  cVar5 = _clock();
  FUN_10018510((int)this);
  cVar6 = _clock();
  puVar10 = *(undefined4 **)((int)this + 0x48);
  local_30a4 = param_3[1] - *param_3 >> 2;
  puVar7 = (undefined4 *)(param_2 + (cVar5 - cVar6));
  puVar23 = (undefined4 *)0x0;
  if (-1 < (int)puVar7) {
    puVar23 = puVar7;
  }
  cVar1 = *(char *)((int)puVar10[1] + 0xd);
  puVar7 = puVar10;
  puVar17 = (undefined4 *)puVar10[1];
  while (cVar1 == '\0') {
    if ((int)puVar17[4] < (int)param_1) {
      puVar8 = (undefined4 *)puVar17[2];
      puVar17 = puVar7;
    }
    else {
      puVar8 = (undefined4 *)*puVar17;
    }
    puVar7 = puVar17;
    puVar17 = puVar8;
    cVar1 = *(char *)((int)puVar8 + 0xd);
  }
  if ((puVar7 == puVar10) || ((int)param_1 < (int)puVar7[4])) {
    puVar7 = puVar10;
  }
  if ((puVar7 == puVar10) || (puVar7[7] == 0)) {
    ppuVar20 = (undefined4 **)0x0;
  }
  else {
    ppuVar20 = (undefined4 **)(uint)*(ushort *)(puVar7[7] + 0x30);
  }
  if (*(byte *)(local_306c + 3) < 5) {
    local_3088 = &local_3074;
    local_18 = (void *)0x0;
    pppuVar26 = &local_3088;
    ppvVar24 = &local_18;
    local_3074 = (undefined4 *)0x1;
    pvVar9 = (void *)FUN_1005f320();
    FUN_10020d90(pvVar9,ppvVar24,pppuVar26);
    local_8 = 0;
    while (local_18 != (void *)0x0) {
      FUN_10007bd0((int *)local_316c);
      local_8._0_1_ = 1;
      local_30 = FUN_1005f320();
      pwVar27 = (wchar_t *)&local_18;
      puVar10 = FUN_100573c0(pwVar27);
      local_2c = puVar10;
      local_28 = (undefined4 *)___uncaught_exceptions();
      local_3070 = local_3070 | 1;
      piVar19 = local_315c;
      local_8 = CONCAT31(local_8._1_3_,2);
      pcVar25 = "Messages in queue: ";
      puVar7 = (undefined4 *)0x10016f7c;
      FUN_1000b420(piVar19,"Messages in queue: ");
      puVar15 = (uint *)((int)local_3148 + *(int *)(local_315c[0] + 4));
      *puVar15 = *puVar15 & 0xfffff3ff | 0x200;
      pwVar28 = 
      L"\xf685᝵ᙨ\x02栀ኰဎとณ\xe810\xf04a\b쒃茌ᣬ趍캘\xffff욃呠㧨＋跿ꑍ\xf1e8Ư였ﱅ贃ꑕ綃Ⴘ䶍ﾼ둵䌏ꑕ柨ƭ茀钍ￏ˿쒃옜ﱅ謂롕廙爐謬ꑍ譂臁ú\x10爀謔ﱉ슃⬣菁ﳀ\xf883༟և\b刀\xe851쾥\x03쒃윈둅"
      ;
      ppuVar29 = ppuVar20;
      FUN_1001e920(local_315c,(ushort)ppuVar20);
      if (puVar10 == (undefined4 *)0x0) {
        ppuVar29 = (undefined4 **)0x216;
        pwVar28 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
        pwVar27 = L"m_pStreamCompound != 0";
        pcVar25 = (char *)0x10016fc2;
        FID_conflict___assert
                  (L"m_pStreamCompound != 0",
                   L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216);
      }
      FUN_10007b10(local_316c,&stack0xffffce74);
      FUN_10031fd0(local_60,puVar7,piVar19,pcVar25,pwVar27,(uint)pwVar28,(uint)ppuVar29);
      local_8._0_1_ = 3;
      pppppppbVar11 = (byte *******)local_60;
      if (0xf < local_4c) {
        pppppppbVar11 = local_60[0];
      }
      FUN_10031d60(local_48,(byte *)pppppppbVar11,(int)local_50);
      local_3070 = local_3070 | 2;
      local_8._0_1_ = 2;
      uVar4 = (undefined1)local_8;
      local_8._0_1_ = 2;
      if (0xf < local_4c) {
        pppppppbVar11 = local_60[0];
        if ((0xfff < local_4c + 1) &&
           (pppppppbVar11 = (byte *******)local_60[0][-1],
           (byte *)0x1f < (byte *)((int)local_60[0] + (-4 - (int)pppppppbVar11)))) {
LAB_10017836:
          local_8._0_1_ = uVar4;
                    /* WARNING: Subroutine does not return */
          FUN_1009cac3();
        }
        FUN_10053fdd(pppppppbVar11);
      }
      local_50 = (undefined4 *)0x0;
      local_4c = 0xf;
      local_60[0] = (byte *******)((uint)local_60[0] & 0xffffff00);
      local_8._0_1_ = 4;
      pppppppbVar11 = (byte *******)local_48;
      if (0xf < local_34) {
        pppppppbVar11 = local_48[0];
      }
      FUN_1000c2f0(puVar10 + 0x18,pppppppbVar11,local_38);
      local_8._0_1_ = 2;
      if (0xf < local_34) {
        uVar18 = local_34 + 1;
        pppppppbVar11 = local_48[0];
        if (0xfff < uVar18) {
          pppppppbVar11 = (byte *******)local_48[0][-1];
          uVar18 = local_34 + 0x24;
          uVar4 = (undefined1)local_8;
          if ((byte *)0x1f < (byte *)((int)local_48[0] + (-4 - (int)pppppppbVar11)))
          goto LAB_10017836;
        }
        local_316c[0] = uVar18;
        FUN_10053fdd(pppppppbVar11);
      }
      local_8._0_1_ = 1;
      local_316c[0] = 0x100170ad;
      FUN_1001d730(&local_30);
      local_8 = (uint)local_8._1_3_ << 8;
      local_316c[0] = 0x100170bc;
      FUN_10004940((int *)local_316c);
    }
    local_8 = 0xffffffff;
    local_18 = (void *)0x0;
  }
  local_3088 = ppuVar20;
  if (param_4 < ppuVar20) {
    local_3088 = param_4;
  }
  ppuVar20 = (undefined4 **)0x0;
  if (local_3088 != (undefined4 **)0x0) {
    do {
      puVar10 = (undefined4 *)FUN_10053c4a(0x1030);
      *(undefined2 *)(puVar10 + 2) = 0;
      *(undefined4 *)((int)puVar10 + 10) = 0;
      *(undefined2 *)((int)puVar10 + 0xe) = 0;
      *puVar10 = 0;
      puVar10[1] = 0;
      local_1c = puVar10;
      _memset(puVar10 + 4,0,0x1020);
      local_3074 = puVar10;
      iVar12 = FUN_10031660(local_306c,(int)param_1,puVar10);
      if (iVar12 != 0) goto LAB_10017818;
      puVar15 = (uint *)local_3090[1];
      if ((uint *)local_3090[2] == puVar15) {
        FUN_10021980(local_3090,puVar15,(uint *)&local_3074);
      }
      else {
        *puVar15 = (uint)puVar10;
        local_3090[1] = local_3090[1] + 4;
      }
      ppuVar20 = (undefined4 **)((int)ppuVar20 + 1);
    } while (ppuVar20 < local_3088);
  }
  if (local_3088 != param_4) {
    local_3064 = 0;
    _memset(local_3060,0,0x3000);
    local_2c = param_1;
    local_28 = puVar23;
    if (puVar23 == (undefined4 *)0x0) {
      pwVar27 = (wchar_t *)0x10;
      local_18 = (void *)FUN_1001d270(local_306c,0x10,(uint *)&local_2c,8,&local_3064,3000);
LAB_10017665:
      if (local_18 != (void *)0x0) goto LAB_10017818;
    }
    else {
      local_307c = __Xtime_get_ticks();
      local_3080 = (undefined4 *)((int)puVar23 >> 0x1f);
      local_3084 = puVar23;
      FUN_10021680((int *)&local_20,(uint *)&local_307c,(uint *)&local_3084);
      puVar10 = (undefined4 *)local_306c[5];
      if (puVar23 <= (undefined4 *)local_306c[5]) {
        puVar10 = puVar23;
      }
      local_307c = ZEXT48(puVar10);
      FUN_100216c0((int *)&local_3084,&local_20,(uint *)&local_307c);
      puVar23 = local_3084;
      local_3074 = puVar10 + 0x2ee;
      lVar3 = CONCAT44(local_1c,local_20);
      local_28 = puVar10;
      do {
        pwVar27 = (wchar_t *)0x10;
        local_18 = (void *)FUN_1001d270(local_306c,0x10,(uint *)&local_2c,8,&local_3064,
                                        (uint)local_3074);
        lVar22 = __Xtime_get_ticks();
        if ((lVar22 < lVar3) && (local_18 != (void *)0x0)) {
          local_20 = 100;
          local_1c = (undefined4 *)0x0;
          FUN_10021700(&local_20);
          lVar22 = __Xtime_get_ticks();
          if (CONCAT44(local_3080,puVar23) < lVar22) {
            local_307c = lVar22 - CONCAT44(local_3080,puVar23);
            puVar13 = FUN_10021650(&local_30a0,(uint *)&local_307c);
            local_28 = *(undefined4 **)puVar13;
            local_3094 = *(int **)((int)puVar13 + 4);
          }
        }
        lVar22 = __Xtime_get_ticks();
        if (lVar3 <= lVar22) goto LAB_10017665;
      } while (local_18 != (void *)0x0);
    }
    local_3094 = (int *)0x0;
    local_3074 = (undefined4 *)0x0;
    local_308c = 0;
    local_30a0._4_4_ = 0;
    if ((short)local_3064 != 0) {
      local_3094._0_2_ = 0;
      local_3066 = 0;
      local_3066 = (ushort)local_3094;
      do {
        puVar23 = local_306c;
        uVar18 = local_308c;
        piVar19 = (int *)((int)local_3060 + (uint)local_3066);
        local_3094 = piVar19;
        uVar2 = *(ushort *)((int)auStack_3052 + (uint)local_3066);
        puVar10 = (undefined4 *)(uint)uVar2;
        local_1c = puVar10;
        if (uVar2 == 0) {
          iVar12 = FUN_10016d40(local_306c,(int)param_1,*piVar19);
          piVar19 = local_3094;
          puVar10 = (undefined4 *)puVar23[0x12];
          cVar1 = *(char *)((int)puVar10[1] + 0xd);
          puVar23 = puVar10;
          puVar7 = (undefined4 *)puVar10[1];
          while (cVar1 == '\0') {
            if ((int)puVar7[4] < iVar12) {
              puVar17 = (undefined4 *)puVar7[2];
              puVar7 = puVar23;
            }
            else {
              puVar17 = (undefined4 *)*puVar7;
            }
            puVar23 = puVar7;
            puVar7 = puVar17;
            cVar1 = *(char *)((int)puVar17 + 0xd);
          }
          if ((puVar23 == puVar10) || (iVar12 < (int)puVar23[4])) {
            puVar23 = puVar10;
          }
          if ((puVar23 == puVar10) || ((void *)puVar23[7] == (void *)0x0)) goto LAB_10017818;
          FUN_10037e90((void *)puVar23[7],(undefined1 *)local_3094);
          local_18 = (void *)0x0;
          local_308c = uVar18 + 1;
        }
        else {
          if (*(byte *)(local_306c + 3) < 5) {
            local_3080 = (undefined4 *)((int)&local_307c + 4);
            local_24 = (void *)0x0;
            ppuVar20 = &local_3080;
            ppvVar24 = &local_24;
            local_307c = CONCAT44(1,(uint)local_307c);
            pvVar9 = (void *)FUN_1005f320();
            FUN_10020d90(pvVar9,ppvVar24,ppuVar20);
            local_8 = 5;
            puVar17 = puVar10;
            puVar7 = local_3080;
            while (local_3080 = puVar17, local_24 != (void *)0x0) {
              FUN_10007bd0((int *)local_316c);
              local_8._0_1_ = 6;
              iVar12 = FUN_1005f320();
              pwVar28 = (wchar_t *)&local_24;
              local_54 = iVar12;
              puVar10 = FUN_100573c0(pwVar28);
              local_50 = puVar10;
              local_4c = ___uncaught_exceptions();
              local_3070 = local_3070 | 4;
              piVar19 = local_315c;
              local_8 = CONCAT31(local_8._1_3_,7);
              pcVar25 = "Error in message: ";
              puVar23 = (undefined4 *)0x10017420;
              FUN_1000b420(piVar19,"Error in message: ");
              puVar15 = (uint *)((int)local_3148 + *(int *)(local_315c[0] + 4));
              *puVar15 = *puVar15 & 0xfffff3ff | 0x200;
              uVar18 = 0x10017453;
              FUN_10036160(local_315c,&local_3080);
              if (puVar10 == (undefined4 *)0x0) {
                uVar18 = 0x216;
                pwVar27 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
                pwVar28 = L"m_pStreamCompound != 0";
                pcVar25 = (char *)0x1001746b;
                FID_conflict___assert
                          (L"m_pStreamCompound != 0",
                           L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp"
                           ,0x216);
              }
              FUN_10007b10(local_316c,&stack0xffffce60);
              FUN_10031fd0(local_48,puVar23,piVar19,pcVar25,pwVar28,(uint)pwVar27,uVar18);
              local_8._0_1_ = 8;
              pppppppbVar11 = (byte *******)local_48;
              if (0xf < local_34) {
                pppppppbVar11 = local_48[0];
              }
              FUN_10031d60(local_30bc,(byte *)pppppppbVar11,local_38);
              local_3070 = local_3070 | 8;
              local_8._0_1_ = 7;
              if (0xf < local_34) {
                pppppppbVar11 = local_48[0];
                if ((0xfff < local_34 + 1) &&
                   (pppppppbVar11 = (byte *******)local_48[0][-1], uVar4 = (undefined1)local_8,
                   (byte *)0x1f < (byte *)((int)local_48[0] + (-4 - (int)pppppppbVar11))))
                goto LAB_10017836;
                FUN_10053fdd(pppppppbVar11);
              }
              local_38 = 0;
              local_34 = 0xf;
              local_48[0] = (byte *******)((uint)local_48[0] & 0xffffff00);
              local_8._0_1_ = 9;
              pwVar27 = (wchar_t *)local_30bc;
              if (0xf < local_30a8) {
                pwVar27 = (wchar_t *)local_30bc[0];
              }
              FUN_1000c2f0(puVar10 + 0x18,pwVar27,local_30ac);
              local_8._0_1_ = 7;
              if (0xf < local_30a8) {
                pppppppuVar16 = local_30bc[0];
                if ((0xfff < local_30a8 + 1) &&
                   (pppppppuVar16 = (undefined4 *******)local_30bc[0][-1],
                   uVar4 = (undefined1)local_8,
                   0x1f < (uint)((int)local_30bc[0] + (-4 - (int)pppppppuVar16))))
                goto LAB_10017836;
                FUN_10053fdd(pppppppuVar16);
              }
              if (iVar12 != 0) {
                local_8._0_1_ = 10;
                local_28 = puVar10;
                uVar18 = ___uncaught_exceptions();
                if (uVar18 <= local_4c) {
                  if (puVar10[0x2c] == 0) {
                    FID_conflict___assert
                              (L"m_record != 0",
                               L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp"
                               ,0x99);
                  }
                  FUN_1000a810(puVar10 + 0x18);
                  pvVar9 = *(void **)(iVar12 + 4);
                  piVar19 = (int *)puVar10[0x2c];
                  if (pvVar9 == (void *)0x0) {
                    FID_conflict___assert
                              (L"px != 0",
                               L"e:\\libs\\boost\\boost_1_65_1\\boost\\smart_ptr\\shared_ptr.hpp",
                               0x2de);
                    pvVar9 = *(void **)(iVar12 + 4);
                  }
                  FUN_1006d0d0(pvVar9,piVar19);
                }
                FUN_10057df0(puVar10);
              }
              local_8 = CONCAT31(local_8._1_3_,5);
              FUN_10004940((int *)local_316c);
              piVar19 = local_3094;
              puVar17 = local_3080;
              puVar10 = local_1c;
              puVar7 = local_3080;
              puVar23 = local_306c;
            }
            local_8 = 0xffffffff;
            puVar15 = (uint *)puVar23[1];
            puVar14 = (uint *)*puVar23;
            local_1c = (undefined4 *)((uint)puVar10 & 0xffff);
            local_3080 = puVar7;
            if (puVar14 != puVar15) {
              do {
                if ((undefined4 *)*puVar14 == local_1c) break;
                puVar14 = puVar14 + 1;
              } while (puVar14 != puVar15);
              if (puVar14 != puVar15) goto LAB_10017687;
            }
            if ((uint *)puVar23[2] == puVar15) {
              FUN_10021980(puVar23,puVar15,(uint *)&local_1c);
            }
            else {
              *puVar15 = (uint)local_1c;
              puVar23[1] = puVar23[1] + 4;
            }
          }
LAB_10017687:
          if ((undefined4 *)((uint)puVar10 & 0xffff) != (undefined4 *)0x27) {
            local_3074 = (undefined4 *)((uint)puVar10 & 0xffff);
          }
        }
        local_3066 = local_3066 + (short)piVar19[2] + 0x10;
        local_30a0._4_4_ = local_30a0._4_4_ + 1;
      } while (local_30a0._4_4_ < (int)(local_3064 & 0xffff));
    }
    uVar18 = (int)param_4 - (int)local_3088;
    if (local_308c <= (uint)((int)param_4 - (int)local_3088)) {
      uVar18 = local_308c;
    }
    uVar21 = 0;
    if (uVar18 != 0) {
      do {
        puVar10 = (undefined4 *)FUN_10053c4a(0x1030);
        *(undefined2 *)(puVar10 + 2) = 0;
        *(undefined4 *)((int)puVar10 + 10) = 0;
        *(undefined2 *)((int)puVar10 + 0xe) = 0;
        *puVar10 = 0;
        puVar10[1] = 0;
        local_28 = puVar10;
        _memset(puVar10 + 4,0,0x1020);
        local_1c = puVar10;
        iVar12 = FUN_10031660(local_306c,(int)param_1,puVar10);
        if (iVar12 != 0) break;
        puVar15 = (uint *)local_3090[1];
        if ((uint *)local_3090[2] == puVar15) {
          FUN_10021980(local_3090,puVar15,(uint *)&local_1c);
        }
        else {
          *puVar15 = (uint)puVar10;
          local_3090[1] = local_3090[1] + 4;
        }
        uVar21 = uVar21 + 1;
      } while (uVar21 < uVar18);
    }
  }
LAB_10017818:
  ExceptionList = local_10;
  __security_check_cookie(local_14 ^ (uint)&stack0xfffffffc);
  return;
}


```

## One level deeper — first few callees of the transport funcs

### FUN_10018510 (size 1144 bytes)
```c

/* WARNING: Removing unreachable block (ram,0x1001870f) */

void __fastcall FUN_10018510(int param_1)

{
  _Mtx_internal_imp_t *p_Var1;
  undefined1 uVar2;
  wchar_t *pwVar3;
  void *pvVar4;
  undefined4 *puVar5;
  uint uVar6;
  int iVar7;
  byte ****ppppbVar8;
  undefined4 ****ppppuVar9;
  uint unaff_EDI;
  undefined4 *in_stack_fffffecc;
  undefined4 uVar10;
  int *piVar11;
  char *pcVar12;
  wchar_t *pwVar13;
  undefined *local_114 [4];
  int local_104 [40];
  int local_64;
  undefined4 *local_60;
  undefined4 local_5c;
  undefined4 ***local_58 [4];
  uint local_48;
  uint local_44;
  undefined4 ***local_40;
  undefined4 ***local_3c;
  byte ***local_38 [4];
  int local_28;
  uint local_24;
  int local_20;
  undefined8 local_1c;
  undefined4 ***local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_100c2f5e;
  local_10 = ExceptionList;
  pwVar3 = (wchar_t *)(DAT_100fc0f4 ^ (uint)&stack0xfffffffc);
  ExceptionList = &local_10;
  local_14 = (undefined4 ***)pwVar3;
  if (*(byte *)(param_1 + 0xc) < 5) {
    local_40 = &local_3c;
    local_1c = local_1c & 0xffffffff;
    ppppuVar9 = &local_40;
    puVar5 = (undefined4 *)((int)&local_1c + 4);
    local_3c = (undefined4 ****)0x1;
    pvVar4 = (void *)FUN_1005f320();
    FUN_10020d90(pvVar4,puVar5,ppppuVar9);
    local_8 = 0;
    while (local_1c._4_4_ != 0) {
      FUN_10007bd0((int *)local_114);
      local_8._0_1_ = 1;
      local_64 = FUN_1005f320();
      puVar5 = FUN_100573c0((int)&local_1c + 4);
      local_60 = puVar5;
      local_5c = ___uncaught_exceptions();
      piVar11 = local_104;
      local_8 = CONCAT31(local_8._1_3_,2);
      pcVar12 = "addToQueue = ";
      uVar10 = 0x100185d8;
      FUN_1000b420(piVar11,"addToQueue = ");
      uVar6 = (uint)*(byte *)(param_1 + 0x174);
      pwVar3 = (wchar_t *)0x100185ee;
      FUN_10024a50(local_104,uVar6);
      if (puVar5 == (undefined4 *)0x0) {
        uVar6 = 0x216;
        pwVar3 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
        pwVar13 = L"m_pStreamCompound != 0";
        piVar11 = (int *)0x10018606;
        FID_conflict___assert
                  (L"m_pStreamCompound != 0",
                   L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216);
        pcVar12 = (char *)pwVar13;
      }
      FUN_10007b10(local_114,&stack0xfffffecc);
      FUN_10031fd0(local_38,in_stack_fffffecc,uVar10,piVar11,pcVar12,(uint)pwVar3,uVar6);
      local_8._0_1_ = 3;
      ppppbVar8 = local_38;
      if (0xf < local_24) {
        ppppbVar8 = (byte ****)local_38[0];
      }
      FUN_10031d60(local_58,(byte *)ppppbVar8,local_28);
      local_8._0_1_ = 2;
      uVar2 = (undefined1)local_8;
      local_8._0_1_ = 2;
      if (0xf < local_24) {
        ppppbVar8 = (byte ****)local_38[0];
        if ((0xfff < local_24 + 1) &&
           (ppppbVar8 = (byte ****)local_38[0][-1],
           (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)ppppbVar8)))) goto LAB_10018983;
        FUN_10053fdd(ppppbVar8);
      }
      local_28 = 0;
      local_24 = 0xf;
      local_38[0] = (byte ***)((uint)local_38[0] & 0xffffff00);
      local_8._0_1_ = 4;
      pwVar3 = (wchar_t *)local_58;
      if (0xf < local_44) {
        pwVar3 = (wchar_t *)local_58[0];
      }
      unaff_EDI = local_48;
      FUN_1000c2f0(puVar5 + 0x18,pwVar3,local_48);
      local_8._0_1_ = 2;
      if (0xf < local_44) {
        local_114[0] = (undefined *)(local_44 + 1);
        ppppuVar9 = (undefined4 ****)local_58[0];
        if ((undefined *)0xfff < local_114[0]) {
          ppppuVar9 = (undefined4 ****)local_58[0][-1];
          local_114[0] = (undefined *)(local_44 + 0x24);
          uVar2 = (undefined1)local_8;
          if (0x1f < (uint)((int)local_58[0] + (-4 - (int)ppppuVar9))) goto LAB_10018983;
        }
        FUN_10053fdd(ppppuVar9);
      }
      local_8._0_1_ = 1;
      local_114[0] = (undefined *)0x100186ea;
      FUN_1001d730(&local_64);
      local_8 = (uint)local_8._1_3_ << 8;
      local_114[0] = (undefined *)0x100186f9;
      FUN_10004940((int *)local_114);
    }
  }
  local_8 = 0xffffffff;
  if (*(char *)(param_1 + 0x174) != '\0') {
    p_Var1 = (_Mtx_internal_imp_t *)(param_1 + 0xe0);
    local_1c = ZEXT48(p_Var1);
    iVar7 = __Mtx_lock(p_Var1);
    if (iVar7 != 0) {
      std::_Throw_C_error(iVar7);
    }
    local_1c._0_5_ = CONCAT14(1,(int)local_1c);
    local_8 = 5;
    if (*(char *)(param_1 + 0x174) != '\0') {
      do {
        iVar7 = __Cnd_wait((_Cnd_internal_imp_t *)(param_1 + 0x138),p_Var1);
        if (iVar7 != 0) {
          std::_Throw_C_error(iVar7);
        }
      } while (*(char *)(param_1 + 0x174) != '\0');
    }
    FUN_1001de30((int *)&local_1c);
    if (*(byte *)(param_1 + 0xc) < 5) {
      local_3c = &local_40;
      local_20 = 0;
      ppppuVar9 = &local_3c;
      piVar11 = &local_20;
      local_40 = (undefined4 ****)0x1;
      pvVar4 = (void *)FUN_1005f320();
      FUN_10020d90(pvVar4,piVar11,ppppuVar9);
      local_8._0_1_ = 6;
      while (local_20 != 0) {
        FUN_10007bd0((int *)local_114);
        local_8._0_1_ = 7;
        local_64 = FUN_1005f320();
        puVar5 = FUN_100573c0(&local_20);
        local_60 = puVar5;
        local_5c = ___uncaught_exceptions();
        piVar11 = local_104;
        local_8 = CONCAT31(local_8._1_3_,8);
        pcVar12 = "addToQueue UNLOCK";
        uVar10 = 0x10018818;
        FUN_1000b420(piVar11,"addToQueue UNLOCK");
        if (puVar5 == (undefined4 *)0x0) {
          unaff_EDI = 0x216;
          pwVar3 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
          pwVar13 = L"m_pStreamCompound != 0";
          piVar11 = (int *)0x10018833;
          FID_conflict___assert
                    (L"m_pStreamCompound != 0",
                     L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216
                    );
          pcVar12 = (char *)pwVar13;
        }
        FUN_10007b10(local_114,&stack0xfffffecc);
        FUN_10031fd0(local_38,in_stack_fffffecc,uVar10,piVar11,pcVar12,(uint)pwVar3,unaff_EDI);
        local_8._0_1_ = 9;
        ppppbVar8 = local_38;
        if (0xf < local_24) {
          ppppbVar8 = (byte ****)local_38[0];
        }
        FUN_10031d60(local_58,(byte *)ppppbVar8,local_28);
        local_8._0_1_ = 8;
        if (0xf < local_24) {
          ppppbVar8 = (byte ****)local_38[0];
          if ((0xfff < local_24 + 1) &&
             (ppppbVar8 = (byte ****)local_38[0][-1], uVar2 = (undefined1)local_8,
             (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)ppppbVar8)))) {
LAB_10018983:
            local_8._0_1_ = uVar2;
                    /* WARNING: Subroutine does not return */
            local_114[0] = &UNK_10018988;
            FUN_1009cac3();
          }
          FUN_10053fdd(ppppbVar8);
        }
        local_28 = 0;
        local_24 = 0xf;
        local_38[0] = (byte ***)((uint)local_38[0] & 0xffffff00);
        local_8._0_1_ = 10;
        pwVar3 = (wchar_t *)local_58;
        if (0xf < local_44) {
          pwVar3 = (wchar_t *)local_58[0];
        }
        unaff_EDI = local_48;
        FUN_1000c2f0(puVar5 + 0x18,pwVar3,local_48);
        local_8._0_1_ = 8;
        if (0xf < local_44) {
          local_114[0] = (undefined *)(local_44 + 1);
          ppppuVar9 = (undefined4 ****)local_58[0];
          if ((undefined *)0xfff < local_114[0]) {
            ppppuVar9 = (undefined4 ****)local_58[0][-1];
            local_114[0] = (undefined *)(local_44 + 0x24);
            uVar2 = (undefined1)local_8;
            if (0x1f < (uint)((int)local_58[0] + (-4 - (int)ppppuVar9))) goto LAB_10018983;
          }
          FUN_10053fdd(ppppuVar9);
        }
        local_48 = 0;
        local_44 = 0xf;
        local_58[0] = (undefined4 ***)((uint)local_58[0] & 0xffffff00);
        local_8._0_1_ = 7;
        local_114[0] = (undefined *)0x10018929;
        FUN_1001d730(&local_64);
        local_8._0_1_ = 6;
        local_114[0] = (undefined *)0x10018938;
        FUN_10004940((int *)local_114);
      }
    }
    local_8 = 0xb;
    if (local_1c._4_1_ != '\0') {
      iVar7 = __Mtx_unlock((int)local_1c);
      if (iVar7 != 0) {
        std::_Throw_C_error(iVar7);
      }
    }
  }
  ExceptionList = local_10;
  __security_check_cookie((uint)local_14 ^ (uint)&stack0xfffffffc);
  return;
}


```

### FUN_1005f320 (size 11 bytes)
```c

int FUN_1005f320(void)

{
  int *piVar1;
  
  piVar1 = (int *)FUN_1005f1b0();
  return *piVar1 + 0xc;
}


```


## Synthesis (2026-05-05)

### Confirmed: device path is `\\.\COMx`

`DAT_100e50a0 = "\\.\\"` — the literal Windows device-namespace prefix. `device_open` builds `\\.\COMx` from the path argument (or just uses the caller's path verbatim if it already starts with `\`).

### Confirmed: device-open settings (already known from round 2, restated)

```c
CreateFileA(path,
    GENERIC_READ | GENERIC_WRITE,   // 0xC0000000
    0,                              // no sharing
    NULL,
    OPEN_EXISTING,                  // 3
    FILE_FLAG_OVERLAPPED,           // 0x40000000
    NULL);

// DCB read, twiddle one bit (rsvd/binary flag), DCB write:
GetCommState(h, &dcb);  // dcb.DCBlength = 0x1c
dcb._4_8_ = (dcb._4_8_ & 0xffffb7bfffffffff) | 0x100000000;
SetCommState(h, &dcb);

// Non-blocking reads, untimed writes:
SetCommTimeouts(h, { ReadIntervalTimeout=1, all-others=0 });

CreateIoCompletionPort(h, channel->iocp_at_0x14, 0, 0);
```

**The driver does not set baud rate.** It inherits whatever the COM port driver below it has configured. This is the smoking gun that the Chipsoft Pro device does its baud negotiation at the USB-CDC layer (in the `.inf` driver / device descriptor), not in this DLL.

### New finding: write path is queue-based, not synchronous

`write_transport` (`FUN_1001a140`) does **not** call `WriteFile`. It:

1. Locks a mutex at `channel->_at_0xb0`.
2. Builds an in-memory **`STRUCT_MESSAGE`** (size `0x1038` — matches the J2534 `PASSTHRU_MSG` layout: 6×u32 header + 4128B `Data[]`).
3. Copies it into a slot of a **ring buffer** at `channel->_at_0x160..0x174`.
4. Calls `__Cnd_signal(channel->_at_0x110)` to wake an I/O thread.
5. Calls `FUN_1001d270(channel, 0x22, msg, msg[3]+0x14, &out, timeout+3000)` — looks like *send command and wait for ack*. The literal `0x22` is suspicious (J2534 internal command code? UDS-style read-by-id? worth confirming).

The xref-string `"Add async message to queue"` (called twice in this function) confirms the architecture.

The actual `WriteFile` happens on a **separate I/O thread** that drains the ring buffer; the ring buffer is what ties this DLL's framing to the wire. Finding the drain thread = finding the on-wire byte format.

### New finding: read path is also queue-based

`read_transport` (`FUN_10016e10`) references `"Messages in queue: "`, `"Error in message: "` — it pops from a queue populated by the same drain thread on the read side. `FUN_1001d270` again appears (so it's bidirectional: send-and-wait).

### Recap of message size

- `PASSTHRU_MSG` per J2534 spec = 24-byte header + 4128 `Data[]` = **4152 = 0x1038**
- Queue slot = 0x1038 bytes (ring buffer copies 0x1038 in line 161)
- Internal "wire" message wraps `PASSTHRU_MSG` with a few extra bytes of timeout/sequence (`local_10a4` + `local_10a0` + `local_109c` + `local_1098` + `local_1096` setup before the `_memset(local_1092, 0, 0x1022)` zero-fill)

The serialization to bytes-on-wire happens **between the queue slot and the WriteFile call** — that's the missing layer.

### Next chase (round 4)

- **`FUN_1001d270`** — the "send and wait" call, used by both write and read transports. High-signal target.
- **The I/O drain thread** — not named in the call graph from this round; need to find threads launched in `device_open` (`CreateIoCompletionPort` is set up but the thread that pumps it isn't visible here). Suggest searching for `CreateThread` xrefs filtered to functions that touch the channel object and walk the ring buffer.
- **`FUN_10018510`** (called by both transports) — likely "drain queue / wait on completion" helper.

### Project-level take

The architecture revealed makes the Android port **simpler** than the worst case in the project plan, *if* the per-message wire framing turns out to be modest. The whole DLL is a thin USB-CDC client with:

- A fixed `PASSTHRU_MSG`-shaped queue (4152-byte fixed slots)
- An I/O thread that serializes/deserializes those slots on a virtual COM port
- Async/IOCP plumbing that's irrelevant on Android (Kotlin coroutines + a single reader thread is enough)

The remaining open question is the per-message envelope on the wire (likely a small fixed header + the `Data[]` payload + maybe a checksum). Round 4 should answer it.

## Channel/pin selection — answered (2026-05-05 from manual + string scan)

Chris flagged that "specific GMLAN modules speak on different channels — you have to switch pin alignment." Confirmed in two layers:

### Layer 1 — registry config (Tech2Win path, consumed by `CSTech2Win.dll`)

Hardware constraint per the EN manual page 6: **the device cannot expose SWCAN-on-pin-1 and HSCAN-on-pins-3-11 simultaneously.** One of the two CAN channels must be dropped. The choice persists in:

- `HKLM\SOFTWARE\CHIPSOFT\Tech2Win\Tech2Win_DropCAN3_11`  (DWORD: 1 = SWCAN on pin 1 active, HSCAN on 3-11 disabled)
- `HKLM\SOFTWARE\CHIPSOFT\Tech2Win\Tech2Win_DropSWCAN1`   (the inverse)
- `HKLM\SOFTWARE\CHIPSOFT\Tech2Win\Tech2Win_UseAsyncMode`

`CST2WinConfig.exe` is just a thin GUI over these reg values (UTF-16 strings in the .rsrc confirm the literal "Drop CAN on pins 3-11" / "Drop Single Wire CAN on pin 1" radio captions write directly to these keys).

For SAAB Trionic 8 — engine ECU SWCAN @ 33.3 kbps on **pin 1** — we want `Tech2Win_DropCAN3_11 = 1` (the default). This is what Chris meant by "switch pin alignment".

There are also per-tier keys for non-Tech2Win flows:
- `HKLM\SOFTWARE\CHIPSOFT\J2534 Lite|Mid|Pro` — used by `j2534_interface.dll`.

Plus `options.json` at `C:\ProgramData\CHIPSOFT_J2534\options.json` for `OpenPort2Mode` and `RemapAUXToPIN`.

### Layer 2 — runtime J2534 IOCTL (the API path we'd use from Android)

`j2534_interface.dll` strings reveal the *standard* J2534-2 mechanism, not a Chipsoft-specific one:

- ProtocolIDs supported: `ISO9141`, `ISO14230`, `CAN`, `ISO15765`, `GM_UART_PS`, **`SW_CAN_PS`**, `SW_ISO15765_PS`, `CAN_PS`, `ISO9141_PS`, `ISO14230_PS`. The `_PS` suffix = "pin select" (J2534-2 per-pin protocols).
- IOCTL config parameter `J1962_PINS` — packed-nibble DWORD per J2534-2 spec; selects which OBD-II pins each CAN channel uses.
- Runtime ordering constraint: error `"Need to set J1962_PINS first"` confirms `PassThruIoctl(SET_CONFIG, J1962_PINS=...)` must be called **before** I/O on certain channels.
- IOCTL `ACTIVE_CHANNELS` exists too (multi-channel arbitration).
- Validation messages: `"Invalid pin configuration for CAN bus"`, `"Invalid SWCAN multiplexor configuration"`, `"Selected J1962 pins are in use"` — all match what J2534-2 prescribes.

### What this means for the Android port

For a SAAB Trionic 8 SecurityAccess unlock from Android, the call sequence is:

```
PassThruOpen()
PassThruConnect(SW_CAN_PS, 0, 33333, &channelID)
PassThruIoctl(channelID, SET_CONFIG, { J1962_PINS = 0x0001 })  // SWCAN on pin 1
PassThruStartMsgFilter(channelID, PASS_FILTER, ...)
PassThruWriteMsgs / PassThruReadMsgs   // UDS 0x10/0x27
```

No need to touch the registry — `SW_CAN_PS` + `J1962_PINS` ioctl handle pin alignment **per channel at runtime**. The registry layer is for the Tech2Win-only path that doesn't expose the J2534 surface to the user.


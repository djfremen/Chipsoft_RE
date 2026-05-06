# Ghidra device-I/O layer — j2534_interface.dll

Round 2: the layer between PassThru*_impl and the Win32 serial APIs.

## write_framer (called by PassThruWriteMsgs_impl) — 0x100321a0

**Strings referenced from this function:**

- _(none)_

```c

/* WARNING: Function: __alloca_probe replaced with injection: alloca_probe */

void __fastcall
FUN_100321a0(undefined *param_1,uint *param_2,uint param_3,undefined4 *param_4,undefined4 *param_5)

{
  int iVar1;
  uint *local_1054;
  undefined8 local_1050;
  uint local_1048 [3];
  undefined2 local_103c;
  undefined4 local_103a;
  undefined1 local_1036 [4138];
  uint local_c;
  
  local_c = DAT_100fc0f4 ^ (uint)&local_1054;
  local_1054 = param_2;
  if (DAT_10104d5c == 0) {
    __security_check_cookie(local_c ^ (uint)&local_1054);
    return;
  }
  local_1048[1] = 0;
  local_103c = 0;
  local_103a = 0;
  local_1048[2] = 0;
  _memset(local_1036,0,0x1022);
  local_1048[0] = param_3;
  local_1050 = 0;
  FUN_10093750(local_1048 + 1,local_1054,0x1030);
  iVar1 = FUN_1001a140(param_1,local_1048,(void **)&local_1050);
  if (iVar1 == 0) {
    *param_4 = (void *)local_1050;
    *param_5 = local_1050._4_4_;
  }
  __security_check_cookie(local_c ^ (uint)&local_1054);
  return;
}


```

## read_framer  (called by PassThruReadMsgs_impl) — 0x1001a540

**Strings referenced from this function:**

- 0x1001a6b8 → 0x100e111c  `timeout = `
- 0x1001a6dd → 0x100e1128  `, readMsgs_ execution time = `
- 0x1001a71a → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001a71f → 0x100e1330  `m_pStreamCompound != 0`
- 0x1001a82e → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001a833 → 0x100e1534  `m_record != 0`
- 0x1001a860 → 0x100e1360  `e:\libs\boost\boost_1_65_1\boost\smart_ptr\shared_ptr.hpp`
- 0x1001a865 → 0x100e13d4  `px != 0`
- 0x1001a95a → 0x100e10f0  `!!cs_read_msg(`
- 0x1001a99e → 0x100e1168  `, message); // `
- 0x1001a9c6 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001a9cb → 0x100e1330  `m_pStreamCompound != 0`
- 0x1001aabb → 0x100e1178  `ThreadID = `
- 0x1001ab15 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001ab1a → 0x100e1534  `m_record != 0`
- 0x1001ab4d → 0x100e1360  `e:\libs\boost\boost_1_65_1\boost\smart_ptr\shared_ptr.hpp`
- 0x1001ab52 → 0x100e13d4  `px != 0`
- 0x1001ac0b → 0x100e1184  `!!// Messages readed: `
- 0x1001ac4f → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001ac54 → 0x100e1330  `m_pStreamCompound != 0`
- 0x1001ad69 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001ad6e → 0x100e1534  `m_record != 0`
- 0x1001ad9b → 0x100e1360  `e:\libs\boost\boost_1_65_1\boost\smart_ptr\shared_ptr.hpp`
- 0x1001ada0 → 0x100e13d4  `px != 0`
- 0x1001aed8 → 0x100e10c8  `!!STRUCT_MESSAGE message;`
- 0x1001aeef → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001aef4 → 0x100e1330  `m_pStreamCompound != 0`
- 0x1001b002 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001b007 → 0x100e1534  `m_record != 0`
- 0x1001b034 → 0x100e1360  `e:\libs\boost\boost_1_65_1\boost\smart_ptr\shared_ptr.hpp`

```c

/* WARNING: Removing unreachable block (ram,0x1001b08f) */
/* WARNING: Removing unreachable block (ram,0x1001b832) */
/* WARNING: Type propagation algorithm not settling */

void FUN_1001a540(undefined4 *param_1,int param_2,int *param_3,undefined4 **param_4)

{
  undefined1 uVar1;
  wchar_t *pwVar2;
  void *pvVar3;
  int iVar4;
  int *******pppppppiVar5;
  uint uVar6;
  DWORD DVar7;
  undefined4 *puVar8;
  int *piVar9;
  uint *puVar10;
  clock_t cVar11;
  byte *******pppppppbVar12;
  uint *puVar13;
  undefined4 **ppuVar14;
  wchar_t *unaff_ESI;
  int *unaff_EDI;
  uint uVar15;
  bool bVar16;
  undefined8 uVar17;
  undefined4 *puVar18;
  char *in_stack_fffffd40;
  int *in_stack_fffffd44;
  byte ******in_stack_fffffd58;
  char *in_stack_fffffd5c;
  int *in_stack_fffffd64;
  char *in_stack_fffffd68;
  byte ******ppppppbVar19;
  char *pcVar20;
  wchar_t *pwVar21;
  char *pcVar22;
  undefined4 uVar23;
  void **ppvVar24;
  int **ppiVar25;
  undefined4 **ppuVar26;
  int *******pppppppiVar27;
  wchar_t *pwVar28;
  void **ppvVar29;
  wchar_t *in_stack_fffffd98;
  byte *******in_stack_fffffd9c;
  wchar_t *in_stack_fffffda0;
  byte *******in_stack_fffffda4;
  byte ******local_248 [5];
  uint auStack_234 [35];
  int local_1a8;
  undefined4 *local_1a4;
  uint local_1a0;
  int local_19c;
  undefined4 *local_198;
  uint local_194;
  int local_190;
  undefined4 *local_18c;
  uint local_188;
  int local_184;
  int *******local_180;
  uint local_17c;
  undefined8 local_178;
  undefined8 local_170;
  int local_168;
  int *******local_164;
  uint local_160;
  int local_15c;
  int *******local_158;
  uint local_154;
  byte *******local_150 [4];
  int *local_140;
  uint local_13c;
  int ******local_138;
  int local_134;
  void *local_130;
  undefined4 *local_12c;
  uint local_128;
  int local_124;
  int *******local_120;
  int *******local_11c;
  undefined4 *local_118;
  int *******local_114;
  int *******local_110;
  int *******local_10c;
  int local_108 [4];
  int local_f8 [5];
  int *local_e4;
  int *local_e0;
  int *local_d4;
  uint *local_d0;
  int *local_c4;
  uint local_b8;
  uint local_b4;
  undefined8 local_58;
  byte *******local_50 [4];
  int *local_40;
  uint local_3c;
  byte *******local_38 [4];
  byte *******local_28;
  uint local_24;
  int *local_20;
  int *******local_1c;
  void *local_18;
  byte *******local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  puVar8 = DAT_10104d5c;
  local_8 = 0xffffffff;
  puStack_c = &LAB_100c33e5;
  local_10 = ExceptionList;
  pwVar2 = (wchar_t *)(DAT_100fc0f4 ^ (uint)&stack0xfffffffc);
  ExceptionList = &local_10;
  uVar15 = 0;
  local_110 = (int *******)0x0;
  local_124 = param_2;
  local_20 = param_3;
  local_118 = DAT_10104d5c;
  param_3[1] = *param_3;
  local_134 = param_2;
  ppuVar14 = param_4;
  local_14 = (byte *******)pwVar2;
  do {
    local_138 = (int ******)_clock();
    uVar17 = __Xtime_get_ticks();
    piVar9 = local_20;
    pwVar21 = (wchar_t *)0x1001a5d1;
    local_170 = uVar17;
    local_120 = (int *******)FUN_10016e10(puVar8,param_1,local_124,local_20,ppuVar14);
    local_178 = __Xtime_get_ticks();
    FUN_10021620((int *)&stack0xfffffd98,(uint *)&local_178,(uint *)&local_170);
    ppvVar24 = (void **)0x1001a60f;
    FUN_100217c0((double *)&stack0xfffffda0);
    if (*(byte *)(puVar8 + 3) < 5) {
      local_114 = (int *******)&local_10c;
      local_18 = (void *)0x0;
      pppppppiVar27 = (int *******)&local_114;
      ppvVar24 = &local_18;
      local_10c = (int *******)0x0;
      pvVar3 = (void *)FUN_1005f320();
      FUN_10020d90(pvVar3,ppvVar24,pppppppiVar27);
      local_8 = 0;
      if (local_18 != (void *)0x0) {
        local_58 = CONCAT44(in_stack_fffffda4,in_stack_fffffda0);
        do {
          FUN_10007bd0((int *)&stack0xfffffda8);
          local_8._0_1_ = 1;
          iVar4 = FUN_1005f320();
          local_184 = iVar4;
          pppppppiVar5 = (int *******)FUN_100573c0(&local_18);
          local_180 = pppppppiVar5;
          local_17c = ___uncaught_exceptions();
          local_8 = CONCAT31(local_8._1_3_,2);
          FUN_1000b420((int *)local_248,"timeout = ");
          FUN_1001e780(local_248,local_124);
          pwVar2 = (wchar_t *)local_248;
          FUN_1000b420((int *)pwVar2,", readMsgs_ execution time = ");
          local_114 = (int *******)FUN_100217f0(&stack0xfffffda8,&local_58);
          pwVar28 = L"s";
          pppppppiVar27 = local_114 + 4;
          unaff_EDI = (int *)0x1001a70e;
          FUN_1000b420((int *)pppppppiVar27,"s");
          if (pppppppiVar5 == (int *******)0x0) {
            in_stack_fffffd9c = (byte *******)0x216;
            in_stack_fffffd98 =
                 L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
            pwVar28 = L"m_pStreamCompound != 0";
            pppppppiVar27 = (int *******)0x1001a729;
            FID_conflict___assert
                      (L"m_pStreamCompound != 0",
                       L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",
                       0x216);
          }
          FUN_10007b10(local_114,&stack0xfffffd88);
          FUN_10031fd0(local_50,(undefined4 *)pwVar2,unaff_EDI,pppppppiVar27,pwVar28,
                       (uint)in_stack_fffffd98,(uint)in_stack_fffffd9c);
          local_8._0_1_ = 3;
          pppppppbVar12 = (byte *******)local_50;
          if (0xf < local_3c) {
            pppppppbVar12 = local_50[0];
          }
          FUN_10031d60(local_38,(byte *)pppppppbVar12,(int)local_40);
          local_8._0_1_ = 2;
          uVar1 = (undefined1)local_8;
          local_8._0_1_ = 2;
          uVar15 = uVar15 | 3;
          if (0xf < local_3c) {
            pppppppbVar12 = local_50[0];
            if ((0xfff < local_3c + 1) &&
               (pppppppbVar12 = (byte *******)local_50[0][-1],
               (byte *)0x1f < (byte *)((int)local_50[0] + (-4 - (int)pppppppbVar12))))
            goto LAB_1001bbc5;
            FUN_10053fdd(pppppppbVar12);
          }
          local_40 = (int *)0x0;
          local_3c = 0xf;
          local_50[0] = (byte *******)((uint)local_50[0] & 0xffffff00);
          local_8._0_1_ = 4;
          in_stack_fffffd98 = (wchar_t *)local_38;
          if (0xf < local_24) {
            in_stack_fffffd98 = (wchar_t *)local_38[0];
          }
          unaff_ESI = 
          L"䗆˼쒃謌\xe055廙爐謬챍譂臁ú\x10爀謔ﱉ슃⬣菁ﳀ\xf883༟쮇\x13刀\xe851韜\x03쒃蔈࿛纄"
          ;
          in_stack_fffffd9c = local_28;
          FUN_1000c2f0((int *)(pppppppiVar5 + 0x18),in_stack_fffffd98,(uint)local_28);
          local_8._0_1_ = 2;
          if (0xf < local_24) {
            in_stack_fffffda4 = local_38[0];
            if ((0xfff < local_24 + 1) &&
               (in_stack_fffffda4 = (byte *******)local_38[0][-1], uVar1 = (undefined1)local_8,
               (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)in_stack_fffffda4))))
            goto LAB_1001bbc5;
            in_stack_fffffda0 = L"쒃蔈࿛纄";
            FUN_10053fdd(in_stack_fffffda4);
          }
          if (iVar4 != 0) {
            local_8._0_1_ = 5;
            local_1c = pppppppiVar5;
            uVar6 = ___uncaught_exceptions();
            if (uVar6 <= local_17c) {
              if (pppppppiVar5[0x2c] == (int ******)0x0) {
                in_stack_fffffda0 = L"m_record != 0";
                in_stack_fffffd9c = (byte *******)0x1001a83d;
                FID_conflict___assert
                          (L"m_record != 0",
                           L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp"
                           ,0x99);
              }
              FUN_1000a810((int *)(pppppppiVar5 + 0x18));
              pvVar3 = *(void **)(iVar4 + 4);
              local_114 = (int *******)pppppppiVar5[0x2c];
              if (pvVar3 == (void *)0x0) {
                in_stack_fffffda0 = L"px != 0";
                in_stack_fffffd9c = (byte *******)0x1001a86f;
                FID_conflict___assert
                          (L"px != 0",
                           L"e:\\libs\\boost\\boost_1_65_1\\boost\\smart_ptr\\shared_ptr.hpp",0x2de)
                ;
                pvVar3 = *(void **)(iVar4 + 4);
              }
              FUN_1006d0d0(pvVar3,(int *)local_114);
            }
            in_stack_fffffda4 = (byte *******)0x1001a887;
            FUN_10057df0(pppppppiVar5);
          }
          local_8 = (uint)local_8._1_3_ << 8;
          FUN_10004940((int *)&stack0xfffffda8);
          piVar9 = local_20;
        } while (local_18 != (void *)0x0);
      }
      local_8 = 0xffffffff;
      if (local_18 != (void *)0x0) {
        FUN_1006cb90(local_18);
      }
      local_10c = (int *******)&local_114;
      pppppppiVar27 = (int *******)&local_10c;
      ppvVar24 = &local_18;
      local_18 = (void *)0x0;
      local_114 = (int *******)0x1;
      if (*piVar9 == piVar9[1]) {
        pvVar3 = (void *)FUN_1005f320();
        FUN_10020d90(pvVar3,ppvVar24,pppppppiVar27);
        local_8 = 6;
        bVar16 = local_18 == (void *)0x0;
        if (!bVar16) {
          do {
            FUN_10007bd0((int *)&stack0xfffffda8);
            local_8._0_1_ = 7;
            local_15c = FUN_1005f320();
            pppppppiVar27 = (int *******)FUN_100573c0(&local_18);
            local_158 = pppppppiVar27;
            local_154 = ___uncaught_exceptions();
            local_8 = CONCAT31(local_8._1_3_,8);
            DVar7 = GetCurrentThreadId();
            FUN_1000b420((int *)local_248,"!!cs_read_msg(");
            FUN_10035840((int *)local_248,(int *)&param_1);
            in_stack_fffffd58 = (byte ******)local_248;
            FUN_1000b420((int *)in_stack_fffffd58,", ");
            FUN_1001e780(local_248,local_124);
            ppppppbVar19 = (byte ******)local_248;
            pcVar20 = ", message); // ";
            in_stack_fffffd68 = (char *)0x1001a9a9;
            FUN_1000b420((int *)ppppppbVar19,", message); // ");
            uVar6 = 0x1001a9bd;
            FUN_10036160((int *)local_248,&local_120);
            if (pppppppiVar27 == (int *******)0x0) {
              uVar6 = 0x216;
              pwVar21 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
              pwVar28 = L"m_pStreamCompound != 0";
              ppppppbVar19 = (byte ******)0x1001a9d5;
              FID_conflict___assert
                        (L"m_pStreamCompound != 0",
                         L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",
                         0x216);
              pcVar20 = (char *)pwVar28;
            }
            local_10c = pppppppiVar27 + 0x18;
            FUN_10007b10(&stack0xfffffda8,&stack0xfffffd64);
            FUN_10031fd0(local_50,in_stack_fffffd64,in_stack_fffffd68,ppppppbVar19,pcVar20,
                         (uint)pwVar21,uVar6);
            local_8._0_1_ = 9;
            pppppppbVar12 = (byte *******)local_50;
            if (0xf < local_3c) {
              pppppppbVar12 = local_50[0];
            }
            in_stack_fffffd5c = (char *)0x1001aa12;
            FUN_10031d60(local_38,(byte *)pppppppbVar12,(int)local_40);
            local_8._0_1_ = 8;
            uVar15 = uVar15 | 0xc;
            if (0xf < local_3c) {
              pppppppbVar12 = local_50[0];
              if ((0xfff < local_3c + 1) &&
                 (pppppppbVar12 = (byte *******)local_50[0][-1], uVar1 = (undefined1)local_8,
                 (byte *)0x1f < (byte *)((int)local_50[0] + (-4 - (int)pppppppbVar12))))
              goto LAB_1001bbc5;
              FUN_10053fdd(pppppppbVar12);
            }
            local_40 = (int *)0x0;
            local_3c = 0xf;
            local_50[0] = (byte *******)((uint)local_50[0] & 0xffffff00);
            local_8._0_1_ = 10;
            pwVar21 = (wchar_t *)local_38;
            if (0xf < local_24) {
              pwVar21 = (wchar_t *)local_38[0];
            }
            FUN_1000c2f0((int *)local_10c,pwVar21,(uint)local_28);
            local_8._0_1_ = 8;
            if (0xf < local_24) {
              pppppppbVar12 = local_38[0];
              if ((0xfff < local_24 + 1) &&
                 (pppppppbVar12 = (byte *******)local_38[0][-1], uVar1 = (undefined1)local_8,
                 (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)pppppppbVar12))))
              goto LAB_1001bbc5;
              in_stack_fffffd9c = (byte *******)0x1001aab8;
              FUN_10053fdd(pppppppbVar12);
            }
            local_28 = (byte *******)0x0;
            local_24 = 0xf;
            local_38[0] = (byte *******)((uint)local_38[0] & 0xffffff00);
            FUN_1001f0b0(pppppppiVar27 + 2,(uint *)"ThreadID = ");
            ppvVar24 = (void **)0x1001aae6;
            FUN_1001e780(local_10c,DVar7);
            if (local_15c != 0) {
              local_8._0_1_ = 0xb;
              local_1c = pppppppiVar27;
              uVar6 = ___uncaught_exceptions();
              if (uVar6 <= local_154) {
                if (pppppppiVar27[0x2c] == (int ******)0x0) {
                  FID_conflict___assert
                            (L"m_record != 0",
                             L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp"
                             ,0x99);
                }
                FUN_1000a810((int *)(pppppppiVar27 + 0x18));
                iVar4 = local_15c;
                local_10c = (int *******)pppppppiVar27[0x2c];
                pvVar3 = *(void **)(local_15c + 4);
                if (pvVar3 == (void *)0x0) {
                  FID_conflict___assert
                            (L"px != 0",
                             L"e:\\libs\\boost\\boost_1_65_1\\boost\\smart_ptr\\shared_ptr.hpp",
                             0x2de);
                  pvVar3 = *(void **)(iVar4 + 4);
                }
                FUN_1006d0d0(pvVar3,(int *)local_10c);
              }
              ppvVar24 = (void **)0x1001ab74;
              FUN_10057df0(pppppppiVar27);
            }
            local_8 = CONCAT31(local_8._1_3_,6);
            FUN_10004940((int *)&stack0xfffffda8);
          } while (local_18 != (void *)0x0);
LAB_1001ade2:
          bVar16 = local_18 == (void *)0x0;
          piVar9 = local_20;
        }
      }
      else {
        pvVar3 = (void *)FUN_1005f320();
        FUN_10020d90(pvVar3,ppvVar24,pppppppiVar27);
        local_8 = 0xc;
        bVar16 = local_18 == (void *)0x0;
        if (!bVar16) {
          do {
            uVar6 = piVar9[1] - *piVar9 >> 2;
            FUN_10007bd0((int *)&stack0xfffffda8);
            local_8._0_1_ = 0xd;
            local_168 = FUN_1005f320();
            pwVar2 = (wchar_t *)&local_18;
            pppppppiVar27 = (int *******)FUN_100573c0(pwVar2);
            local_164 = pppppppiVar27;
            local_160 = ___uncaught_exceptions();
            ppppppbVar19 = (byte ******)local_248;
            local_8 = CONCAT31(local_8._1_3_,0xe);
            pcVar20 = "!!// Messages readed: ";
            puVar8 = (undefined4 *)0x1001ac16;
            FUN_1000b420((int *)ppppppbVar19,"!!// Messages readed: ");
            *(uint *)((int)auStack_234 + (int)local_248[0][1]) =
                 *(uint *)((int)auStack_234 + (int)local_248[0][1]) & 0xfffff3ff | 0x200;
            pwVar21 = (wchar_t *)0x1001ac46;
            FUN_1001e780(local_248,uVar6);
            if (pppppppiVar27 == (int *******)0x0) {
              uVar6 = 0x216;
              pwVar21 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
              pwVar2 = L"m_pStreamCompound != 0";
              pcVar20 = (char *)0x1001ac5e;
              FID_conflict___assert
                        (L"m_pStreamCompound != 0",
                         L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",
                         0x216);
            }
            FUN_10007b10(&stack0xfffffda8,&stack0xfffffd78);
            FUN_10031fd0(local_38,puVar8,ppppppbVar19,pcVar20,pwVar2,(uint)pwVar21,uVar6);
            local_8._0_1_ = 0xf;
            pppppppbVar12 = (byte *******)local_38;
            if (0xf < local_24) {
              pppppppbVar12 = local_38[0];
            }
            pwVar21 = (wchar_t *)local_28;
            FUN_10031d60(local_50,(byte *)pppppppbVar12,(int)local_28);
            local_8._0_1_ = 0xe;
            uVar15 = uVar15 | 0x30;
            if (0xf < local_24) {
              pppppppbVar12 = local_38[0];
              if ((0xfff < local_24 + 1) &&
                 (pppppppbVar12 = (byte *******)local_38[0][-1], uVar1 = (undefined1)local_8,
                 (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)pppppppbVar12))))
              goto LAB_1001bbc5;
              FUN_10053fdd(pppppppbVar12);
            }
            local_28 = (byte *******)0x0;
            local_24 = 0xf;
            local_38[0] = (byte *******)((uint)local_38[0] & 0xffffff00);
            local_8._0_1_ = 0x10;
            pwVar2 = (wchar_t *)local_50;
            if (0xf < local_3c) {
              pwVar2 = (wchar_t *)local_50[0];
            }
            ppvVar24 = (void **)0x1001acfe;
            unaff_EDI = local_40;
            FUN_1000c2f0((int *)(pppppppiVar27 + 0x18),pwVar2,(uint)local_40);
            local_8._0_1_ = 0xe;
            if (0xf < local_3c) {
              pppppppbVar12 = local_50[0];
              if ((0xfff < local_3c + 1) &&
                 (pppppppbVar12 = (byte *******)local_50[0][-1], uVar1 = (undefined1)local_8,
                 (byte *)0x1f < (byte *)((int)local_50[0] + (-4 - (int)pppppppbVar12))))
              goto LAB_1001bbc5;
              unaff_ESI = L"쒃謈鲵\xfffe藿࿶纄";
              FUN_10053fdd(pppppppbVar12);
            }
            iVar4 = local_168;
            if (local_168 != 0) {
              local_8._0_1_ = 0x11;
              local_1c = pppppppiVar27;
              uVar6 = ___uncaught_exceptions();
              if (uVar6 <= local_160) {
                if (pppppppiVar27[0x2c] == (int ******)0x0) {
                  unaff_ESI = L"m_record != 0";
                  unaff_EDI = (int *)0x1001ad78;
                  FID_conflict___assert
                            (L"m_record != 0",
                             L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp"
                             ,0x99);
                }
                FUN_1000a810((int *)(pppppppiVar27 + 0x18));
                pvVar3 = *(void **)(iVar4 + 4);
                local_10c = (int *******)pppppppiVar27[0x2c];
                if (pvVar3 == (void *)0x0) {
                  unaff_ESI = L"px != 0";
                  unaff_EDI = (int *)0x1001adaa;
                  FID_conflict___assert
                            (L"px != 0",
                             L"e:\\libs\\boost\\boost_1_65_1\\boost\\smart_ptr\\shared_ptr.hpp",
                             0x2de);
                  pvVar3 = *(void **)(iVar4 + 4);
                }
                FUN_1006d0d0(pvVar3,(int *)local_10c);
              }
              FUN_10057df0(pppppppiVar27);
            }
            local_8 = CONCAT31(local_8._1_3_,0xc);
            in_stack_fffffd98 =
                 L"䖋诬\xe45d삅蔏﷞\xffff삅䗇￼\xffff瓿倉鷨ԝ茀ӄ떋ﻬ\xffff΋䮋褄\xf885\xfffe觿\xe84d섻萏޴"
            ;
            FUN_10004940((int *)&stack0xfffffda8);
            piVar9 = local_20;
          } while (local_18 != (void *)0x0);
          goto LAB_1001ade2;
        }
      }
      local_8 = 0xffffffff;
      puVar8 = local_118;
      if (!bVar16) {
        ppvVar24 = (void **)0x1001adf3;
        FUN_1006cb90(local_18);
        puVar8 = local_118;
      }
    }
    local_10c = (int *******)*piVar9;
    local_1c = (int *******)piVar9[1];
    if (local_10c != local_1c) {
      do {
        pppppppiVar27 = (int *******)*local_10c;
        local_110 = pppppppiVar27;
        if (*(char *)((int)puVar8 + 0x26a) == '\0') {
          if (*(byte *)(puVar8 + 3) < 5) {
            local_11c = (int *******)&local_114;
            local_18 = (void *)0x0;
            pppppppiVar5 = (int *******)&local_11c;
            ppvVar24 = &local_18;
            local_114 = (int *******)0x1;
            pvVar3 = (void *)FUN_1005f320();
            FUN_10020d90(pvVar3,ppvVar24,pppppppiVar5);
            local_8 = 0x12;
            pwVar2 = (wchar_t *)in_stack_fffffd40;
            while (local_18 != (void *)0x0) {
              FUN_10007bd0((int *)&stack0xfffffda8);
              local_8._0_1_ = 0x13;
              iVar4 = FUN_1005f320();
              pwVar28 = (wchar_t *)&local_18;
              local_190 = iVar4;
              puVar8 = FUN_100573c0(pwVar28);
              local_18c = puVar8;
              local_188 = ___uncaught_exceptions();
              ppppppbVar19 = (byte ******)local_248;
              local_8 = CONCAT31(local_8._1_3_,0x14);
              pcVar20 = "!!STRUCT_MESSAGE message;";
              puVar18 = (undefined4 *)0x1001aee3;
              FUN_1000b420((int *)ppppppbVar19,"!!STRUCT_MESSAGE message;");
              if (puVar8 == (undefined4 *)0x0) {
                in_stack_fffffd44 = (int *)0x216;
                pwVar2 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
                pwVar28 = L"m_pStreamCompound != 0";
                pcVar20 = (char *)0x1001aefe;
                FID_conflict___assert
                          (L"m_pStreamCompound != 0",
                           L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp"
                           ,0x216);
              }
              FUN_10007b10(&stack0xfffffda8,&stack0xfffffd30);
              FUN_10031fd0(local_38,puVar18,ppppppbVar19,pcVar20,pwVar28,(uint)pwVar2,
                           (uint)in_stack_fffffd44);
              local_8._0_1_ = 0x15;
              pppppppbVar12 = (byte *******)local_38;
              if (0xf < local_24) {
                pppppppbVar12 = local_38[0];
              }
              FUN_10031d60(local_50,(byte *)pppppppbVar12,(int)local_28);
              local_8._0_1_ = 0x14;
              uVar15 = uVar15 | 0xc0;
              if (0xf < local_24) {
                pppppppbVar12 = local_38[0];
                if ((0xfff < local_24 + 1) &&
                   (pppppppbVar12 = (byte *******)local_38[0][-1], uVar1 = (undefined1)local_8,
                   (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)pppppppbVar12))))
                goto LAB_1001bbc5;
                FUN_10053fdd(pppppppbVar12);
              }
              local_28 = (byte *******)0x0;
              local_24 = 0xf;
              local_38[0] = (byte *******)((uint)local_38[0] & 0xffffff00);
              local_8._0_1_ = 0x16;
              pwVar2 = (wchar_t *)local_50;
              if (0xf < local_3c) {
                pwVar2 = (wchar_t *)local_50[0];
              }
              in_stack_fffffd44 = local_40;
              FUN_1000c2f0(puVar8 + 0x18,pwVar2,(uint)local_40);
              local_8._0_1_ = 0x14;
              if (0xf < local_3c) {
                pppppppbVar12 = local_50[0];
                if ((0xfff < local_3c + 1) &&
                   (pppppppbVar12 = (byte *******)local_50[0][-1], uVar1 = (undefined1)local_8,
                   (byte *)0x1f < (byte *)((int)local_50[0] + (-4 - (int)pppppppbVar12))))
                goto LAB_1001bbc5;
                FUN_10053fdd(pppppppbVar12);
              }
              if (iVar4 != 0) {
                local_58 = CONCAT44(puVar8,(undefined4)local_58);
                local_8._0_1_ = 0x17;
                uVar6 = ___uncaught_exceptions();
                if (uVar6 <= local_188) {
                  if (puVar8[0x2c] == 0) {
                    in_stack_fffffd44 = (int *)0x1001b011;
                    FID_conflict___assert
                              (L"m_record != 0",
                               L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp"
                               ,0x99);
                  }
                  FUN_1000a810(puVar8 + 0x18);
                  pvVar3 = *(void **)(iVar4 + 4);
                  local_11c = (int *******)puVar8[0x2c];
                  if (pvVar3 == (void *)0x0) {
                    in_stack_fffffd44 = (int *)0x1001b043;
                    FID_conflict___assert
                              (L"px != 0",
                               L"e:\\libs\\boost\\boost_1_65_1\\boost\\smart_ptr\\shared_ptr.hpp",
                               0x2de);
                    pvVar3 = *(void **)(iVar4 + 4);
                  }
                  FUN_1006d0d0(pvVar3,(int *)local_11c);
                }
                FUN_10057df0(puVar8);
              }
              local_8 = CONCAT31(local_8._1_3_,0x12);
              FUN_10004940((int *)&stack0xfffffda8);
              pppppppiVar27 = local_110;
              puVar8 = local_118;
            }
            local_8 = 0xffffffff;
          }
          *(undefined1 *)((int)puVar8 + 0x26a) = 1;
        }
        _memset(local_108,0,0xb0);
        FUN_10007bd0(local_108);
        local_8 = 0x18;
        DVar7 = GetCurrentThreadId();
        pcVar20 = ", message);";
        in_stack_fffffd40 = "!!cs_read_msg(";
        piVar9 = FUN_1000b420(local_f8,"!!cs_read_msg(");
        piVar9 = FUN_10035840(piVar9,(int *)&param_1);
        in_stack_fffffd44 = (int *)0x1001b107;
        piVar9 = FUN_1000b420(piVar9,pcVar20);
        in_stack_fffffd58 = (byte ******)FUN_1001e780(piVar9,in_stack_fffffd58);
        piVar9 = FUN_1000b420((int *)in_stack_fffffd58,in_stack_fffffd5c);
        piVar9 = FUN_1000b420(piVar9,in_stack_fffffd68);
        FUN_1001e780(piVar9,DVar7);
        local_11c = *(int ********)((int)pppppppiVar27 + 10);
        local_110 = (int *******)*pppppppiVar27;
        local_130 = (void *)0x0;
        local_12c = (undefined4 *)0x0;
        local_128 = 0;
        FUN_1000c570(&local_130,(uint *)(pppppppiVar27 + 4),
                     *(ushort *)(pppppppiVar27 + 2) + 0x10 + (int)pppppppiVar27);
        in_stack_fffffd64 = local_f8;
        local_8._0_1_ = 0x19;
        in_stack_fffffd68 = " // Readed message: ";
        piVar9 = FUN_1000b420(in_stack_fffffd64," // Readed message: ");
        piVar9 = FUN_10035840(piVar9,(int *)&local_110);
        piVar9 = FUN_1000b420(piVar9,(char *)pwVar21);
        piVar9 = FUN_10037da0(piVar9,(int *)&local_130);
        piVar9 = FUN_1000b420(piVar9,(char *)ppvVar24);
        if (piVar9 == (int *)0x0) {
          iVar4 = 0;
        }
        else {
          iVar4 = *(int *)(*piVar9 + 4) + (int)piVar9;
        }
        *(uint *)(iVar4 + 0x14) = *(uint *)(iVar4 + 0x14) & 0xfffff9ff | 0x800;
        pwVar28 = *(wchar_t **)((int)pppppppiVar27 + 10);
        ppvVar24 = (void **)&DAT_100e0e4c;
        piVar9 = FUN_1000b420(piVar9,"0x");
        unaff_EDI = FUN_1001e780(piVar9,unaff_EDI);
        pwVar2 = 
        L"쒃贈\xe895\xfffe诿\xe8c8젨\x01䗆᣼趋ﻔ\xffff즅乴開ﻜ\xffff솋턫嬨က";
        piVar9 = FUN_1000b420(unaff_EDI,(char *)unaff_ESI);
        in_stack_fffffd98 = L"䗆᣼趋ﻔ\xffff즅乴開ﻜ\xffff솋턫嬨က";
        FUN_10037a40(piVar9,(uint *)&local_11c);
        local_8._0_1_ = 0x18;
        if (local_130 != (void *)0x0) {
          in_stack_fffffd98 = (wchar_t *)(local_128 - (int)local_130);
          pvVar3 = local_130;
          if ((byte *******)0xfff < in_stack_fffffd98) {
            pvVar3 = *(void **)((int)local_130 + -4);
            in_stack_fffffd98 = (wchar_t *)((int)in_stack_fffffd98 + 0x23);
            uVar1 = (undefined1)local_8;
            if (0x1f < (uint)((int)local_130 + (-4 - (int)pvVar3))) goto LAB_1001bbc5;
          }
          unaff_ESI = L"쒃윈풅\xfffeÿ";
          FUN_10053fdd(pvVar3);
          local_130 = (void *)0x0;
          local_12c = (undefined4 *)0x0;
          local_128 = 0;
        }
        puVar8 = local_118;
        if (*(byte *)(local_118 + 3) < 5) {
          local_11c = (int *******)&local_110;
          local_18 = (void *)0x0;
          in_stack_fffffd98 = (wchar_t *)&local_11c;
          ppvVar29 = &local_18;
          local_110 = (int *******)0x1;
          pvVar3 = (void *)FUN_1005f320();
          unaff_ESI = L"綃ì萏˚";
          FUN_10020d90(pvVar3,ppvVar29,(undefined4 *)in_stack_fffffd98);
          while (local_18 != (void *)0x0) {
            local_8 = CONCAT31(local_8._1_3_,0x1b);
            local_110 = (int *******)(uVar15 | 0x200);
            local_40 = (int *)0x0;
            local_3c = 0xf;
            local_50[0] = (byte *******)((uint)local_50[0] & 0xffffff00);
            if (((local_b4 & 2) == 0) && (uVar6 = *local_d0, uVar6 != 0)) {
              if (uVar6 < local_b8) {
                uVar6 = local_b8;
              }
              puVar13 = (uint *)*local_e0;
              uVar6 = uVar6 - (int)puVar13;
LAB_1001b349:
              FUN_100030d0(local_50,puVar13,uVar6);
            }
            else if (((local_b4 & 4) == 0) && (*local_d4 != 0)) {
              puVar13 = (uint *)*local_e4;
              uVar6 = (*local_c4 - (int)puVar13) + *local_d4;
              goto LAB_1001b349;
            }
            local_8 = 0x1c;
            FUN_10007bd0((int *)&stack0xfffffda8);
            local_8._0_1_ = 0x1d;
            iVar4 = FUN_1005f320();
            ppvVar24 = &local_18;
            local_19c = iVar4;
            puVar8 = FUN_100573c0(ppvVar24);
            local_198 = puVar8;
            local_194 = ___uncaught_exceptions();
            local_8 = CONCAT31(local_8._1_3_,0x1e);
            pppppppbVar12 = (byte *******)local_50;
            if (0xf < local_3c) {
              pppppppbVar12 = local_50[0];
            }
            piVar9 = local_40;
            FUN_1000c2f0((int *)local_248,pppppppbVar12,(uint)local_40);
            if (puVar8 == (undefined4 *)0x0) {
              unaff_EDI = (int *)0x216;
              pwVar2 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
              pwVar28 = L"m_pStreamCompound != 0";
              ppvVar24 = (void **)0x1001b3d4;
              FID_conflict___assert
                        (L"m_pStreamCompound != 0",
                         L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",
                         0x216);
            }
            FUN_10007b10(&stack0xfffffda8,&stack0xfffffd78);
            FUN_10031fd0(local_38,pppppppbVar12,piVar9,ppvVar24,pwVar28,(uint)pwVar2,(uint)unaff_EDI
                        );
            local_8._0_1_ = 0x1f;
            pppppppbVar12 = (byte *******)local_38;
            if (0xf < local_24) {
              pppppppbVar12 = local_38[0];
            }
            pwVar21 = (wchar_t *)local_28;
            FUN_10031d60(local_150,(byte *)pppppppbVar12,(int)local_28);
            local_8._0_1_ = 0x1e;
            uVar15 = uVar15 | 0xd00;
            if (0xf < local_24) {
              pppppppbVar12 = local_38[0];
              if ((0xfff < local_24 + 1) &&
                 (pppppppbVar12 = (byte *******)local_38[0][-1], uVar1 = (undefined1)local_8,
                 (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)pppppppbVar12))))
              goto LAB_1001bbc5;
              FUN_10053fdd(pppppppbVar12);
            }
            local_28 = (byte *******)0x0;
            local_24 = 0xf;
            local_38[0] = (byte *******)((uint)local_38[0] & 0xffffff00);
            local_8._0_1_ = 0x20;
            pwVar2 = (wchar_t *)local_150;
            if (0xf < local_13c) {
              pwVar2 = (wchar_t *)local_150[0];
            }
            pwVar28 = (wchar_t *)(puVar8 + 0x18);
            ppvVar24 = (void **)0x1001b486;
            unaff_EDI = local_140;
            FUN_1000c2f0((int *)pwVar28,pwVar2,(uint)local_140);
            local_8._0_1_ = 0x1e;
            if (0xf < local_13c) {
              pppppppbVar12 = local_150[0];
              if ((0xfff < local_13c + 1) &&
                 (pppppppbVar12 = (byte *******)local_150[0][-1], uVar1 = (undefined1)local_8,
                 (byte *)0x1f < (byte *)((int)local_150[0] + (-4 - (int)pppppppbVar12))))
              goto LAB_1001bbc5;
              unaff_ESI = L"쒃蔈瓛襾끵䗆⇼⧨И㤀炅\xfffe狿荡낾";
              FUN_10053fdd(pppppppbVar12);
            }
            if (iVar4 != 0) {
              local_58 = CONCAT44(puVar8,(undefined4)local_58);
              local_8._0_1_ = 0x21;
              uVar6 = ___uncaught_exceptions();
              if (uVar6 <= local_194) {
                if (puVar8[0x2c] == 0) {
                  unaff_ESI = L"m_record != 0";
                  unaff_EDI = (int *)0x1001b4fc;
                  FID_conflict___assert
                            (L"m_record != 0",
                             L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp"
                             ,0x99);
                }
                FUN_1000a810(puVar8 + 0x18);
                pvVar3 = *(void **)(iVar4 + 4);
                local_110 = (int *******)puVar8[0x2c];
                if (pvVar3 == (void *)0x0) {
                  unaff_ESI = L"px != 0";
                  unaff_EDI = (int *)0x1001b52e;
                  FID_conflict___assert
                            (L"px != 0",
                             L"e:\\libs\\boost\\boost_1_65_1\\boost\\smart_ptr\\shared_ptr.hpp",
                             0x2de);
                  pvVar3 = *(void **)(iVar4 + 4);
                }
                FUN_1006d0d0(pvVar3,(int *)local_110);
              }
              FUN_10057df0(puVar8);
            }
            in_stack_fffffd98 = L"䗆᫼喋菈ჺⱲ䶋䊴솋嬨က";
            FUN_10004940((int *)&stack0xfffffda8);
            local_8._0_1_ = 0x1a;
            puVar8 = local_118;
            if (0xf < local_3c) {
              in_stack_fffffd98 = (wchar_t *)(local_3c + 1);
              pppppppbVar12 = local_50[0];
              if ((byte *******)0xfff < in_stack_fffffd98) {
                pppppppbVar12 = (byte *******)local_50[0][-1];
                in_stack_fffffd98 = (wchar_t *)(local_3c + 0x24);
                uVar1 = (undefined1)local_8;
                if ((byte *)0x1f < (byte *)((int)local_50[0] + (-4 - (int)pppppppbVar12)))
                goto LAB_1001bbc5;
              }
              unaff_ESI = (wchar_t *)0x1001b589;
              FUN_10053fdd(pppppppbVar12);
              puVar8 = local_118;
            }
          }
        }
        local_8 = 0xffffffff;
        FUN_10004940(local_108);
        local_10c = local_10c + 1;
      } while (local_10c != local_1c);
    }
    pppppppiVar27 = local_120;
    if (*(byte *)(puVar8 + 3) < 5) {
      local_110 = (int *******)&local_1c;
      local_18 = (void *)0x0;
      pppppppiVar27 = (int *******)&local_110;
      ppvVar24 = &local_18;
      local_1c = (int *******)0x1;
      pvVar3 = (void *)FUN_1005f320();
      FUN_10020d90(pvVar3,ppvVar24,pppppppiVar27);
      local_8 = 0x22;
      pppppppiVar27 = local_120;
      while (local_120 = pppppppiVar27, local_18 != (void *)0x0) {
        FUN_10007bd0((int *)&stack0xfffffda8);
        local_8._0_1_ = 0x23;
        iVar4 = FUN_1005f320();
        pwVar21 = (wchar_t *)&local_18;
        local_1a8 = iVar4;
        puVar8 = FUN_100573c0(pwVar21);
        local_1a4 = puVar8;
        local_1a0 = ___uncaught_exceptions();
        ppppppbVar19 = (byte ******)local_248;
        local_8 = CONCAT31(local_8._1_3_,0x24);
        pcVar20 = "!!// Result = ";
        puVar18 = (undefined4 *)0x1001b666;
        FUN_1000b420((int *)ppppppbVar19,"!!// Result = ");
        uVar6 = 0x1001b67a;
        FUN_10036160((int *)local_248,&local_120);
        if (puVar8 == (undefined4 *)0x0) {
          uVar6 = 0x216;
          pwVar2 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
          pwVar21 = L"m_pStreamCompound != 0";
          pcVar20 = (char *)0x1001b692;
          FID_conflict___assert
                    (L"m_pStreamCompound != 0",
                     L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216
                    );
        }
        FUN_10007b10(&stack0xfffffda8,&stack0xfffffd78);
        FUN_10031fd0(local_38,puVar18,ppppppbVar19,pcVar20,pwVar21,(uint)pwVar2,uVar6);
        local_8._0_1_ = 0x25;
        pppppppbVar12 = (byte *******)local_38;
        if (0xf < local_24) {
          pppppppbVar12 = local_38[0];
        }
        FUN_10031d60(local_150,(byte *)pppppppbVar12,(int)local_28);
        local_8._0_1_ = 0x24;
        uVar15 = uVar15 | 0x3000;
        if (0xf < local_24) {
          pppppppbVar12 = local_38[0];
          if ((0xfff < local_24 + 1) &&
             (pppppppbVar12 = (byte *******)local_38[0][-1], uVar1 = (undefined1)local_8,
             (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)pppppppbVar12))))
          goto LAB_1001bbc5;
          FUN_10053fdd(pppppppbVar12);
        }
        local_28 = (byte *******)0x0;
        local_24 = 0xf;
        local_38[0] = (byte *******)((uint)local_38[0] & 0xffffff00);
        local_8._0_1_ = 0x26;
        pwVar2 = (wchar_t *)local_150;
        if (0xf < local_13c) {
          pwVar2 = (wchar_t *)local_150[0];
        }
        unaff_EDI = local_140;
        FUN_1000c2f0(puVar8 + 0x18,pwVar2,(uint)local_140);
        local_8._0_1_ = 0x24;
        if (0xf < local_13c) {
          pppppppbVar12 = local_150[0];
          if ((0xfff < local_13c + 1) &&
             (pppppppbVar12 = (byte *******)local_150[0][-1], uVar1 = (undefined1)local_8,
             (byte *)0x1f < (byte *)((int)local_150[0] + (-4 - (int)pppppppbVar12))))
          goto LAB_1001bbc5;
          unaff_ESI = L"쒃蔈瓛襾끵䗆⟼毨Е㤀撅\xfffe狿荡낾";
          FUN_10053fdd(pppppppbVar12);
        }
        if (iVar4 != 0) {
          local_58 = CONCAT44(puVar8,(undefined4)local_58);
          local_8._0_1_ = 0x27;
          uVar6 = ___uncaught_exceptions();
          if (uVar6 <= local_1a0) {
            if (puVar8[0x2c] == 0) {
              unaff_ESI = L"m_record != 0";
              unaff_EDI = (int *)0x1001b7ba;
              FID_conflict___assert
                        (L"m_record != 0",
                         L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",
                         0x99);
            }
            FUN_1000a810(puVar8 + 0x18);
            pvVar3 = *(void **)(iVar4 + 4);
            local_110 = (int *******)puVar8[0x2c];
            if (pvVar3 == (void *)0x0) {
              unaff_ESI = L"px != 0";
              unaff_EDI = (int *)0x1001b7ec;
              FID_conflict___assert
                        (L"px != 0",
                         L"e:\\libs\\boost\\boost_1_65_1\\boost\\smart_ptr\\shared_ptr.hpp",0x2de);
              pvVar3 = *(void **)(iVar4 + 4);
            }
            FUN_1006d0d0(pvVar3,(int *)local_110);
          }
          FUN_10057df0(puVar8);
        }
        local_8 = CONCAT31(local_8._1_3_,0x22);
        in_stack_fffffd98 = (wchar_t *)0x1001b816;
        FUN_10004940((int *)&stack0xfffffda8);
        puVar8 = local_118;
        pppppppiVar27 = local_120;
      }
      local_8 = 0xffffffff;
      puVar13 = (uint *)puVar8[1];
      puVar10 = (uint *)*puVar8;
      local_1c = pppppppiVar27;
      if (puVar10 != puVar13) {
        do {
          if ((int *******)*puVar10 == pppppppiVar27) break;
          puVar10 = puVar10 + 1;
        } while (puVar10 != puVar13);
        if (puVar10 != puVar13) goto LAB_1001b880;
      }
      if ((uint *)puVar8[2] == puVar13) {
        FUN_10021980(puVar8,puVar13,(uint *)&local_1c);
      }
      else {
        *puVar13 = (uint)pppppppiVar27;
        puVar8[1] = puVar8[1] + 4;
      }
    }
LAB_1001b880:
    if ((pppppppiVar27 != (int *******)0x0) && (pppppppiVar27 != (int *******)0xc8))
    goto LAB_1001bb95;
    ppuVar14 = (undefined4 **)((int)param_4 - (local_20[1] - *local_20 >> 2));
    if (ppuVar14 != (undefined4 **)0x0) {
      cVar11 = _clock();
      local_134 = (int)local_138 + (local_134 - cVar11);
    }
  } while ((0 < local_134) && (ppuVar14 != (undefined4 **)0x0));
  if (*(byte *)(puVar8 + 3) < 5) {
    local_1c = &local_138;
    local_20 = (int *)0x0;
    pppppppiVar27 = (int *******)&local_1c;
    ppiVar25 = &local_20;
    local_138 = (int ******)0x1;
    pvVar3 = (void *)FUN_1005f320();
    FUN_10020d90(pvVar3,ppiVar25,pppppppiVar27);
    local_8 = 0x28;
    while (local_20 != (int *)0x0) {
      FUN_10007bd0((int *)&stack0xfffffda8);
      local_8._0_1_ = 0x29;
      local_130 = (void *)FUN_1005f320();
      puVar8 = FUN_100573c0(&local_20);
      local_12c = puVar8;
      local_128 = ___uncaught_exceptions();
      local_8 = CONCAT31(local_8._1_3_,0x2a);
      pcVar22 = "dynTimeout = ";
      FUN_1000b420((int *)local_248,"dynTimeout = ");
      iVar4 = local_134;
      *(uint *)((int)auStack_234 + (int)local_248[0][1]) =
           *(uint *)((int)auStack_234 + (int)local_248[0][1]) & 0xfffff3ff | 0x200;
      FUN_10008360(local_248,iVar4);
      ppppppbVar19 = (byte ******)local_248;
      pcVar20 = ", readedCountLeft = ";
      uVar23 = 0x1001b9ba;
      FUN_1000b420((int *)ppppppbVar19,", readedCountLeft = ");
      pwVar2 = (wchar_t *)0x1001b9c9;
      ppuVar26 = ppuVar14;
      FUN_1001e780(local_248,ppuVar14);
      if (puVar8 == (undefined4 *)0x0) {
        ppuVar26 = (undefined4 **)0x216;
        pwVar2 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
        pwVar21 = L"m_pStreamCompound != 0";
        ppppppbVar19 = (byte ******)0x1001b9e1;
        FID_conflict___assert
                  (L"m_pStreamCompound != 0",
                   L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216);
        pcVar20 = (char *)pwVar21;
      }
      FUN_10007b10(&stack0xfffffda8,&stack0xfffffd78);
      FUN_10031fd0(local_38,(undefined4 *)pcVar22,uVar23,ppppppbVar19,pcVar20,(uint)pwVar2,
                   (uint)ppuVar26);
      local_8._0_1_ = 0x2b;
      pppppppbVar12 = (byte *******)local_38;
      if (0xf < local_24) {
        pppppppbVar12 = local_38[0];
      }
      FUN_10031d60(local_150,(byte *)pppppppbVar12,(int)local_28);
      local_8._0_1_ = 0x2a;
      if (0xf < local_24) {
        pppppppbVar12 = local_38[0];
        if ((0xfff < local_24 + 1) &&
           (pppppppbVar12 = (byte *******)local_38[0][-1], uVar1 = (undefined1)local_8,
           (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)pppppppbVar12)))) {
LAB_1001bbc5:
          local_8._0_1_ = uVar1;
                    /* WARNING: Subroutine does not return */
          FUN_1009cac3();
        }
        FUN_10053fdd(pppppppbVar12);
      }
      local_28 = (byte *******)0x0;
      local_24 = 0xf;
      local_38[0] = (byte *******)((uint)local_38[0] & 0xffffff00);
      local_8._0_1_ = 0x2c;
      pppppppbVar12 = (byte *******)local_150;
      if (0xf < local_13c) {
        pppppppbVar12 = local_150[0];
      }
      FUN_1000c2f0(puVar8 + 0x18,pppppppbVar12,(uint)local_140);
      local_8._0_1_ = 0x2a;
      if (0xf < local_13c) {
        pppppppbVar12 = local_150[0];
        if ((0xfff < local_13c + 1) &&
           (pppppppbVar12 = (byte *******)local_150[0][-1], uVar1 = (undefined1)local_8,
           (byte *)0x1f < (byte *)((int)local_150[0] + (-4 - (int)pppppppbVar12))))
        goto LAB_1001bbc5;
        FUN_10053fdd(pppppppbVar12);
      }
      if (local_130 != (void *)0x0) {
        local_58 = CONCAT44(puVar8,(undefined4)local_58);
        local_8._0_1_ = 0x2d;
        uVar15 = ___uncaught_exceptions();
        if (uVar15 <= local_128) {
          if (puVar8[0x2c] == 0) {
            FID_conflict___assert
                      (L"m_record != 0",
                       L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",
                       0x99);
          }
          FUN_1000a810(puVar8 + 0x18);
          local_1c = (int *******)puVar8[0x2c];
          pvVar3 = *(void **)((int)local_130 + 4);
          if (pvVar3 == (void *)0x0) {
            FID_conflict___assert
                      (L"px != 0",L"e:\\libs\\boost\\boost_1_65_1\\boost\\smart_ptr\\shared_ptr.hpp"
                       ,0x2de);
            pvVar3 = *(void **)((int)local_130 + 4);
          }
          FUN_1006d0d0(pvVar3,(int *)local_1c);
        }
        FUN_10057df0(puVar8);
      }
      local_8 = CONCAT31(local_8._1_3_,0x28);
      FUN_10004940((int *)&stack0xfffffda8);
    }
  }
LAB_1001bb95:
  ExceptionList = local_10;
  __security_check_cookie((uint)local_14 ^ (uint)&stack0xfffffffc);
  return;
}


```

## device_open  (CreateFileA + Comm setup) — 0x10039460

**Strings referenced from this function:**

- _(none)_

```c

void FUN_10039460(DWORD *param_1,int *param_2,uint *param_3,DWORD *param_4)

{
  undefined *puVar1;
  uint *puVar2;
  LPCSTR ***ppppCVar3;
  DWORD DVar4;
  undefined **ppuVar5;
  BOOL BVar6;
  HANDLE pvVar7;
  void *pvVar8;
  void *local_b0 [5];
  uint local_9c;
  void *local_98 [4];
  undefined4 local_88;
  uint local_84;
  int *local_7c;
  int *local_78;
  DWORD *local_74;
  HANDLE local_70;
  _DCB local_6c;
  _COMMTIMEOUTS local_50;
  LPCSTR **local_3c;
  uint uStack_38;
  uint uStack_34;
  uint uStack_30;
  undefined8 local_2c;
  uint local_24;
  undefined1 *puStack_20;
  void *local_1c;
  undefined1 *puStack_18;
  undefined4 uStack_14;
  
  puStack_20 = &stack0xfffffffc;
  uStack_14 = 0xffffffff;
  puStack_18 = &LAB_100c53ec;
  local_1c = ExceptionList;
  local_24 = DAT_100fc0f4 ^ (uint)&stack0xfffffff0;
  ExceptionList = &local_1c;
  local_70 = (HANDLE)0x0;
  local_74 = param_1;
  local_78 = param_2;
  if (*param_2 != -1) {
    puStack_20 = &stack0xfffffffc;
    puVar1 = FUN_1000ded0();
    *param_4 = 1;
    param_4[1] = (DWORD)puVar1;
    *param_1 = 1;
    param_1[1] = (DWORD)puVar1;
    goto LAB_100397cf;
  }
  puVar2 = param_3;
  if (0xf < param_3[5]) {
    puVar2 = (uint *)*param_3;
  }
  if ((char)*puVar2 == '\\') {
    puStack_20 = &stack0xfffffffc;
    puVar2 = FUN_10007a40(local_b0,param_3);
    pvVar7 = (HANDLE)0x1;
  }
  else {
    puVar2 = FUN_10003210(local_98,(uint *)&DAT_100e50a0,param_3);
    pvVar7 = (HANDLE)0x2;
  }
  local_3c = (LPCSTR **)*puVar2;
  uStack_38 = puVar2[1];
  uStack_34 = puVar2[2];
  uStack_30 = puVar2[3];
  local_2c = *(undefined8 *)(puVar2 + 4);
  puVar2[4] = 0;
  puVar2[5] = 0xf;
  *(undefined1 *)puVar2 = 0;
  if (((uint)pvVar7 & 2) != 0) {
    local_70 = (HANDLE)((uint)pvVar7 & 0xfffffffd);
    if (0xf < local_84) {
      pvVar8 = local_98[0];
      if ((0xfff < local_84 + 1) &&
         (pvVar8 = *(void **)((int)local_98[0] + -4),
         0x1f < (uint)((int)local_98[0] + (-4 - (int)pvVar8)))) {
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pvVar8);
    }
    local_88 = 0;
    local_84 = 0xf;
    local_98[0] = (void *)((uint)local_98[0] & 0xffffff00);
    pvVar7 = local_70;
  }
  if ((((uint)pvVar7 & 1) != 0) && (0xf < local_9c)) {
    pvVar8 = local_b0[0];
    if ((0xfff < local_9c + 1) &&
       (pvVar8 = *(void **)((int)local_b0[0] + -4),
       0x1f < (uint)((int)local_b0[0] + (-4 - (int)pvVar8)))) {
                    /* WARNING: Subroutine does not return */
      FUN_1009cac3();
    }
    FUN_10053fdd(pvVar8);
  }
  ppppCVar3 = &local_3c;
  if (0xf < local_2c._4_4_) {
    ppppCVar3 = (LPCSTR ***)local_3c;
  }
  local_70 = CreateFileA((LPCSTR)ppppCVar3,0xc0000000,0,(LPSECURITY_ATTRIBUTES)0x0,3,0x40000000,
                         (HANDLE)0x0);
  if (local_70 == (HANDLE)0xffffffff) {
    DVar4 = GetLastError();
  }
  else {
    local_6c.DCBlength = 0x1c;
    local_6c._4_8_ = 0;
    local_6c.wReserved = 0;
    local_6c.XonLim = 0;
    local_6c.XoffLim = 0;
    local_6c.ByteSize = '\0';
    local_6c.Parity = '\0';
    local_6c.StopBits = '\0';
    local_6c.XonChar = '\0';
    local_6c.XoffChar = '\0';
    local_6c.ErrorChar = '\0';
    local_6c.EofChar = '\0';
    local_6c.EvtChar = '\0';
    local_6c.wReserved1 = 0;
    BVar6 = GetCommState(local_70,&local_6c);
    if (BVar6 == 0) {
      DVar4 = GetLastError();
      CloseHandle(local_70);
    }
    else {
      local_6c._4_8_ = local_6c._4_8_ & 0xffffb7bfffffffff | 0x100000000;
      BVar6 = SetCommState(local_70,&local_6c);
      if (BVar6 == 0) {
        DVar4 = GetLastError();
        CloseHandle(local_70);
      }
      else {
        local_50.ReadIntervalTimeout = 1;
        local_50.ReadTotalTimeoutMultiplier = 0;
        local_50.ReadTotalTimeoutConstant = 0;
        local_50.WriteTotalTimeoutMultiplier = 0;
        local_50.WriteTotalTimeoutConstant = 0;
        BVar6 = SetCommTimeouts(local_70,&local_50);
        if (BVar6 != 0) {
          if (*local_78 == -1) {
            pvVar7 = CreateIoCompletionPort(local_70,*(HANDLE *)(*local_7c + 0x14),0,0);
            if (pvVar7 == (HANDLE)0x0) {
              DVar4 = GetLastError();
              ppuVar5 = FUN_10055c00();
              *param_4 = DVar4;
              param_1 = local_74;
            }
            else {
              ppuVar5 = FUN_10055c00();
              *param_4 = 0;
            }
            param_4[1] = (DWORD)ppuVar5;
            if (*param_4 == 0) {
              *local_78 = (int)local_70;
              ppuVar5 = FUN_10055c00();
              *param_4 = 0;
              param_4[1] = (DWORD)ppuVar5;
            }
            else {
              CloseHandle(local_70);
            }
          }
          else {
            puVar1 = FUN_1000ded0();
            *param_4 = 1;
            param_4[1] = (DWORD)puVar1;
            CloseHandle(local_70);
          }
          *param_1 = *param_4;
          param_1[1] = param_4[1];
          if (0xf < local_2c._4_4_) {
            ppppCVar3 = (LPCSTR ***)local_3c;
            if ((local_2c._4_4_ + 1 < 0x1000) ||
               (ppppCVar3 = (LPCSTR ***)local_3c[-1],
               (LPCSTR)((int)local_3c + (-4 - (int)ppppCVar3)) < (LPCSTR)0x20)) {
              FUN_10053fdd(ppppCVar3);
              goto LAB_100397cf;
            }
            goto LAB_100397f9;
          }
          goto LAB_100397cf;
        }
        DVar4 = GetLastError();
        CloseHandle(local_70);
      }
    }
  }
  ppuVar5 = FUN_10055c00();
  *param_4 = DVar4;
  param_4[1] = (DWORD)ppuVar5;
  *local_74 = DVar4;
  local_74[1] = (DWORD)ppuVar5;
  if (0xf < local_2c._4_4_) {
    ppppCVar3 = (LPCSTR ***)local_3c;
    if ((0xfff < local_2c._4_4_ + 1) &&
       (ppppCVar3 = (LPCSTR ***)local_3c[-1],
       (LPCSTR)0x1f < (LPCSTR)((int)local_3c + (-4 - (int)ppppCVar3)))) {
LAB_100397f9:
                    /* WARNING: Subroutine does not return */
      FUN_1009cac3();
    }
    FUN_10053fdd(ppppCVar3);
  }
LAB_100397cf:
  ExceptionList = local_1c;
  __security_check_cookie(local_24 ^ (uint)&stack0xfffffff0);
  return;
}


```

## device_reconfig (GetCommState + SetCommState) — 0x10039800

**Strings referenced from this function:**

- _(none)_

```c

void FUN_10039800(DWORD *param_1,undefined4 *param_2,undefined *param_3,undefined4 param_4,
                 DWORD *param_5)

{
  BOOL BVar1;
  DWORD DVar2;
  int *piVar3;
  undefined **ppuVar4;
  undefined1 local_34 [4];
  undefined4 local_30;
  code *local_2c;
  _DCB local_28;
  uint local_c;
  
  local_c = DAT_100fc0f4 ^ (uint)&stack0xfffffffc;
  local_2c = (code *)param_3;
  local_30 = param_4;
  local_28.BaudRate = 0;
  local_28._8_4_ = 0;
  local_28.wReserved = 0;
  local_28.XonLim = 0;
  local_28.XoffLim = 0;
  local_28.ByteSize = '\0';
  local_28.Parity = '\0';
  local_28.StopBits = '\0';
  local_28.XonChar = '\0';
  local_28.XoffChar = '\0';
  local_28.ErrorChar = '\0';
  local_28.EofChar = '\0';
  local_28.EvtChar = '\0';
  local_28.wReserved1 = 0;
  local_28.DCBlength = 0x1c;
  BVar1 = GetCommState((HANDLE)*param_2,&local_28);
  if (BVar1 == 0) {
LAB_10039851:
    DVar2 = GetLastError();
  }
  else {
    piVar3 = (int *)(*local_2c)(local_34,local_30,&local_28,param_5);
    if (*piVar3 != 0) {
      *param_1 = *param_5;
      ppuVar4 = (undefined **)param_5[1];
      goto LAB_10039899;
    }
    BVar1 = SetCommState((HANDLE)*param_2,&local_28);
    if (BVar1 == 0) goto LAB_10039851;
    DVar2 = 0;
  }
  ppuVar4 = FUN_10055c00();
  *param_5 = DVar2;
  param_5[1] = (DWORD)ppuVar4;
  *param_1 = DVar2;
LAB_10039899:
  param_1[1] = (DWORD)ppuVar4;
  __security_check_cookie(local_c ^ (uint)&stack0xfffffffc);
  return;
}


```

## device_write_async (WriteFile + GetOverlappedResult) — 0x1003dca0

**Strings referenced from this function:**

- _(none)_

```c

void FUN_1003dca0(int *param_1,undefined4 param_2,undefined4 param_3,int param_4,DWORD *param_5)

{
  uint uVar1;
  undefined **ppuVar2;
  BOOL BVar3;
  DWORD DVar4;
  char *pcVar5;
  code *pcVar6;
  uint nNumberOfBytesToWrite;
  LPCVOID local_24;
  _OVERLAPPED local_20;
  char local_c;
  undefined3 uStack_b;
  uint local_8;
  
  local_8 = DAT_100fc0f4 ^ (uint)&stack0xfffffffc;
  uVar1 = *(uint *)(param_4 + 0x18);
  local_c = '\x01';
  if (uVar1 != 0) {
    local_c = *(char *)(param_4 + 8);
  }
  uStack_b = 0;
  local_24 = *(LPCVOID *)(param_4 + 0xc);
  nNumberOfBytesToWrite = *(uint *)(param_4 + 0x10);
  pcVar5 = *(char **)(param_4 + 0x14);
LAB_1003dce6:
  if (uVar1 <= nNumberOfBytesToWrite) {
    nNumberOfBytesToWrite = uVar1;
  }
  do {
    if (local_c != '\0') {
      local_24 = (LPCVOID)0x0;
      nNumberOfBytesToWrite = 0;
LAB_1003dd20:
      if (*param_1 == -1) {
        ppuVar2 = FUN_10055c00();
        param_5[1] = (DWORD)ppuVar2;
        *param_5 = 0x2719;
        __security_check_cookie(local_8 ^ (uint)&stack0xfffffffc);
        return;
      }
      if (nNumberOfBytesToWrite == 0) {
        ppuVar2 = FUN_10055c00();
        param_5[1] = (DWORD)ppuVar2;
        *param_5 = 0;
        __security_check_cookie(local_8 ^ (uint)&stack0xfffffffc);
        return;
      }
      local_20.Internal = 0;
      local_20.InternalHigh = 0;
      local_20.u.s.Offset = 0;
      local_20.u.s.OffsetHigh = 0;
      local_20.hEvent = CreateEventW((LPSECURITY_ATTRIBUTES)0x0,1,0,(LPCWSTR)0x0);
      if (local_20.hEvent == (HANDLE)0x0) {
        DVar4 = GetLastError();
        ppuVar2 = FUN_10055c00();
        *param_5 = DVar4;
        pcVar6 = GetLastError_exref;
        param_5[1] = (DWORD)ppuVar2;
      }
      else {
        local_20.hEvent = (HANDLE)((uint)local_20.hEvent | 1);
        pcVar6 = GetLastError_exref;
      }
      if (*param_5 != 0) goto LAB_1003ddfc;
      BVar3 = WriteFile((HANDLE)*param_1,local_24,nNumberOfBytesToWrite,(LPDWORD)0x0,&local_20);
      if (BVar3 == 0) {
        DVar4 = (*pcVar6)();
        if (DVar4 == 0x3e5) goto LAB_1003de1c;
        ppuVar2 = FUN_10055c00();
        *param_5 = DVar4;
      }
      else {
LAB_1003de1c:
        local_c = '\0';
        uStack_b = 0;
        BVar3 = GetOverlappedResult((HANDLE)*param_1,&local_20,(LPDWORD)&local_c,1);
        if (BVar3 != 0) {
          ppuVar2 = FUN_10055c00();
          *param_5 = 0;
          param_5[1] = (DWORD)ppuVar2;
          if (local_20.hEvent != (HANDLE)0x0) {
            CloseHandle(local_20.hEvent);
          }
          __security_check_cookie(local_8 ^ (uint)&stack0xfffffffc);
          return;
        }
        DVar4 = (*pcVar6)();
        ppuVar2 = FUN_10055c00();
        *param_5 = DVar4;
      }
      param_5[1] = (DWORD)ppuVar2;
LAB_1003ddfc:
      if (local_20.hEvent != (HANDLE)0x0) {
        CloseHandle(local_20.hEvent);
      }
      __security_check_cookie(local_8 ^ (uint)&stack0xfffffffc);
      return;
    }
    if (nNumberOfBytesToWrite != 0) goto LAB_1003dd20;
    if ((pcVar5 != (char *)(param_4 + 8)) && (uVar1 != 0)) break;
    local_c = '\x01';
  } while( true );
  local_24 = *(LPCVOID *)pcVar5;
  nNumberOfBytesToWrite = *(uint *)(pcVar5 + 4);
  pcVar5 = pcVar5 + 8;
  goto LAB_1003dce6;
}


```

## device_read  (ReadFile, non-CRT) — 0x100392f0

**Strings referenced from this function:**

- _(none)_

```c

void __thiscall
FUN_100392f0(void *this,int *param_1,undefined4 param_2,undefined4 param_3,undefined4 *param_4,
            LPOVERLAPPED param_5)

{
  DWORD *pDVar1;
  int iVar2;
  undefined4 *puVar3;
  DWORD DVar4;
  BOOL BVar5;
  undefined4 *local_c;
  uint local_8;
  
  local_8 = DAT_100fc0f4 ^ (uint)&stack0xfffffffc;
  local_c = param_4;
  if (param_1[1] == 0) {
    DVar4 = GetCurrentThreadId();
    param_1[1] = DVar4;
  }
  else {
    DVar4 = GetCurrentThreadId();
    if (param_1[1] != DVar4) {
      param_1[1] = -1;
    }
  }
  puVar3 = local_c;
  LOCK();
  *(int *)(*(int *)this + 0x18) = *(int *)(*(int *)this + 0x18) + 1;
  UNLOCK();
  if (*param_1 == -1) {
    FUN_10038a20(*(void **)this,param_5,0x2719,0);
    __security_check_cookie(local_8 ^ (uint)&stack0xfffffffc);
    return;
  }
  if (local_c[1] == 0) {
    FUN_10038a20(*(void **)this,param_5,0,0);
    __security_check_cookie(local_8 ^ (uint)&stack0xfffffffc);
    return;
  }
  (param_5->u).s.Offset = 0;
  (param_5->u).s.OffsetHigh = 0;
  pDVar1 = local_c + 1;
  local_c = (undefined4 *)0x0;
  BVar5 = ReadFile((HANDLE)*param_1,(LPVOID)*puVar3,*pDVar1,(LPDWORD)&local_c,param_5);
  DVar4 = GetLastError();
  if (((BVar5 == 0) && (DVar4 != 0x3e5)) && (DVar4 != 0xea)) {
    FUN_10038a20(*(void **)this,param_5,DVar4,(DWORD)local_c);
    __security_check_cookie(local_8 ^ (uint)&stack0xfffffffc);
    return;
  }
  iVar2 = *(int *)this;
  LOCK();
  DVar4 = param_5[1].u.s.Offset;
  if (DVar4 == 0) {
    param_5[1].u.s.Offset = 1;
    DVar4 = 0;
  }
  UNLOCK();
  if ((DVar4 == 1) &&
     (BVar5 = PostQueuedCompletionStatus(*(HANDLE *)(iVar2 + 0x14),0,2,param_5), BVar5 == 0)) {
    EnterCriticalSection((LPCRITICAL_SECTION)(iVar2 + 0x38));
    param_5[1].Internal = 0;
    if (*(int *)(iVar2 + 0x58) == 0) {
      *(LPOVERLAPPED *)(iVar2 + 0x54) = param_5;
    }
    else {
      *(LPOVERLAPPED *)(*(int *)(iVar2 + 0x58) + 0x14) = param_5;
    }
    *(LPOVERLAPPED *)(iVar2 + 0x58) = param_5;
    LOCK();
    *(undefined4 *)(iVar2 + 0x34) = 1;
    UNLOCK();
    LeaveCriticalSection((LPCRITICAL_SECTION)(iVar2 + 0x38));
  }
  __security_check_cookie(local_8 ^ (uint)&stack0xfffffffc);
  return;
}


```

## purge_a (PurgeComm) — 0x10018990

**Strings referenced from this function:**

- 0x10018a5d → 0x100e0ff0  `com port close_`
- 0x10018a74 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x10018a79 → 0x100e1330  `m_pStreamCompound != 0`

```c

void __fastcall FUN_10018990(int param_1)

{
  wchar_t *pwVar1;
  void *this;
  undefined4 *puVar2;
  byte ****ppppbVar3;
  undefined4 ****ppppuVar4;
  uint unaff_ESI;
  undefined4 *in_stack_fffffedc;
  undefined4 uVar5;
  int *piVar6;
  undefined4 **ppuVar7;
  char *pcVar8;
  wchar_t *pwVar9;
  int local_10c;
  int local_fc [40];
  undefined4 ***local_5c [4];
  uint local_4c;
  uint local_48;
  int local_44;
  undefined4 *local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 *local_34;
  byte ***local_30 [4];
  int local_20;
  uint local_1c;
  int local_18;
  undefined4 ***local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  local_8 = -1;
  puStack_c = &LAB_100c2fbb;
  local_10 = ExceptionList;
  pwVar1 = (wchar_t *)(DAT_100fc0f4 ^ (uint)&stack0xfffffffc);
  ExceptionList = &local_10;
  local_14 = (undefined4 ***)pwVar1;
  PurgeComm(*(HANDLE *)(param_1 + 0x194),0xf);
  FUN_10039bf0(param_1 + 0x188);
  if (*(byte *)(param_1 + 0xc) < 5) {
    local_34 = &local_38;
    local_18 = 0;
    ppuVar7 = &local_34;
    piVar6 = &local_18;
    local_38 = 1;
    this = (void *)FUN_1005f320();
    FUN_10020d90(this,piVar6,ppuVar7);
    local_8 = 0;
    while (local_18 != 0) {
      FUN_10007bd0(&local_10c);
      local_8._0_1_ = 1;
      local_44 = FUN_1005f320();
      puVar2 = FUN_100573c0(&local_18);
      local_40 = puVar2;
      local_3c = ___uncaught_exceptions();
      piVar6 = local_fc;
      local_8 = CONCAT31(local_8._1_3_,2);
      pcVar8 = "com port close_";
      uVar5 = 0x10018a68;
      FUN_1000b420(piVar6,"com port close_");
      if (puVar2 == (undefined4 *)0x0) {
        unaff_ESI = 0x216;
        pwVar1 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
        pwVar9 = L"m_pStreamCompound != 0";
        piVar6 = (int *)0x10018a83;
        FID_conflict___assert
                  (L"m_pStreamCompound != 0",
                   L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216);
        pcVar8 = (char *)pwVar9;
      }
      FUN_10007b10(&local_10c,&stack0xfffffedc);
      FUN_10031fd0(local_30,in_stack_fffffedc,uVar5,piVar6,pcVar8,(uint)pwVar1,unaff_ESI);
      local_8._0_1_ = 3;
      ppppbVar3 = local_30;
      if (0xf < local_1c) {
        ppppbVar3 = (byte ****)local_30[0];
      }
      FUN_10031d60(local_5c,(byte *)ppppbVar3,local_20);
      local_8._0_1_ = 2;
      if (0xf < local_1c) {
        ppppbVar3 = (byte ****)local_30[0];
        if ((0xfff < local_1c + 1) &&
           (ppppbVar3 = (byte ****)local_30[0][-1],
           (byte *)0x1f < (byte *)((int)local_30[0] + (-4 - (int)ppppbVar3)))) goto LAB_10018b96;
        FUN_10053fdd(ppppbVar3);
      }
      local_20 = 0;
      local_1c = 0xf;
      local_30[0] = (byte ***)((uint)local_30[0] & 0xffffff00);
      local_8._0_1_ = 4;
      pwVar1 = (wchar_t *)local_5c;
      if (0xf < local_48) {
        pwVar1 = (wchar_t *)local_5c[0];
      }
      unaff_ESI = local_4c;
      FUN_1000c2f0(puVar2 + 0x18,pwVar1,local_4c);
      local_8._0_1_ = 2;
      if (0xf < local_48) {
        ppppuVar4 = (undefined4 ****)local_5c[0];
        if ((0xfff < local_48 + 1) &&
           (ppppuVar4 = (undefined4 ****)local_5c[0][-1],
           0x1f < (uint)((int)local_5c[0] + (-4 - (int)ppppuVar4)))) {
LAB_10018b96:
          local_8._0_1_ = 2;
                    /* WARNING: Subroutine does not return */
          FUN_1009cac3();
        }
        local_10c = 0x10018b54;
        FUN_10053fdd(ppppuVar4);
      }
      local_8._0_1_ = 1;
      FUN_1001d730(&local_44);
      local_8 = (uint)local_8._1_3_ << 8;
      FUN_10004940(&local_10c);
    }
  }
  ExceptionList = local_10;
  __security_check_cookie((uint)local_14 ^ (uint)&stack0xfffffffc);
  return;
}


```

## purge_b (PurgeComm) — 0x10018ba0

**Strings referenced from this function:**

- 0x10018c5d → 0x100e1000  `!!cs_open_device();`
- 0x10018c74 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x10018c79 → 0x100e1330  `m_pStreamCompound != 0`
- 0x10018eed → 0x100e1014  `device = `
- 0x10018f1f → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x10018f24 → 0x100e1330  `m_pStreamCompound != 0`
- 0x1001916d → 0x100e1020  `Device in use`
- 0x10019184 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x10019189 → 0x100e1330  `m_pStreamCompound != 0`
- 0x100193cd → 0x100e1030  `Device not connected`
- 0x100193e4 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x100193e9 → 0x100e1330  `m_pStreamCompound != 0`

```c

/* WARNING: Removing unreachable block (ram,0x100192a5) */
/* WARNING: Removing unreachable block (ram,0x10019505) */
/* WARNING: Removing unreachable block (ram,0x10018d8c) */
/* WARNING: Removing unreachable block (ram,0x10019040) */
/* WARNING: Type propagation algorithm not settling */

void __fastcall FUN_10018ba0(undefined4 *param_1)

{
  uint uVar1;
  uint *puVar2;
  undefined1 uVar3;
  wchar_t *pwVar4;
  void *pvVar5;
  undefined4 *puVar6;
  uint **ppuVar7;
  int iVar8;
  byte *******pppppppbVar9;
  undefined4 *puVar10;
  int *extraout_ECX;
  uint *puVar11;
  int *extraout_ECX_00;
  wchar_t *unaff_EBX;
  wchar_t *unaff_ESI;
  uint *unaff_EDI;
  undefined4 *in_stack_fffffe78;
  undefined4 *in_stack_fffffe8c;
  uint *puVar12;
  undefined4 uVar13;
  void **ppvVar14;
  int *piVar15;
  uint ***pppuVar16;
  char *pcVar17;
  wchar_t *pwVar18;
  undefined4 *******pppppppuVar19;
  wchar_t *pwVar20;
  uint *in_stack_fffffeac;
  int local_144 [40];
  undefined1 local_a4 [16];
  byte *******local_94 [4];
  uint *local_84;
  uint local_80;
  undefined1 local_7c [4];
  int local_78;
  undefined4 *local_74;
  undefined4 local_70;
  undefined4 *******local_6c;
  uint *local_68;
  int local_64;
  undefined4 *local_60;
  uint *local_5c;
  byte *******local_50 [4];
  undefined4 *local_40;
  uint local_3c;
  byte *******local_38 [4];
  uint *local_28;
  uint local_24;
  undefined4 *******local_20;
  uint **local_1c;
  void *local_18;
  byte *******local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  local_8._0_1_ = 0xff;
  local_8._1_3_ = 0xffffff;
  puStack_c = &LAB_100c30c5;
  local_10 = ExceptionList;
  pwVar4 = (wchar_t *)(DAT_100fc0f4 ^ (uint)&stack0xfffffffc);
  ExceptionList = &local_10;
  local_14 = (byte *******)pwVar4;
  if (*(byte *)(param_1 + 3) < 5) {
    local_1c = &local_68;
    local_18 = (void *)0x0;
    pppuVar16 = &local_1c;
    ppvVar14 = &local_18;
    local_68 = (uint *)0x1;
    pvVar5 = (void *)FUN_1005f320();
    FUN_10020d90(pvVar5,ppvVar14,pppuVar16);
    local_8 = 0;
    while (local_18 != (void *)0x0) {
      FUN_10007bd0((int *)&stack0xfffffeac);
      local_8._0_1_ = 1;
      local_64 = FUN_1005f320();
      puVar6 = FUN_100573c0(&local_18);
      local_60 = puVar6;
      local_5c = (uint *)___uncaught_exceptions();
      piVar15 = local_144;
      local_8 = CONCAT31(local_8._1_3_,2);
      pcVar17 = "!!cs_open_device();";
      uVar13 = 0x10018c68;
      FUN_1000b420(piVar15,"!!cs_open_device();");
      if (puVar6 == (undefined4 *)0x0) {
        unaff_EDI = (uint *)0x216;
        pwVar4 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
        pwVar18 = L"m_pStreamCompound != 0";
        piVar15 = (int *)0x10018c83;
        FID_conflict___assert
                  (L"m_pStreamCompound != 0",
                   L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216);
        pcVar17 = (char *)pwVar18;
      }
      FUN_10007b10(&stack0xfffffeac,&stack0xfffffe8c);
      FUN_10031fd0(local_50,in_stack_fffffe8c,uVar13,piVar15,pcVar17,(uint)pwVar4,(uint)unaff_EDI);
      local_8._0_1_ = 3;
      pppppppbVar9 = (byte *******)local_50;
      if (0xf < local_3c) {
        pppppppbVar9 = local_50[0];
      }
      FUN_10031d60(local_38,(byte *)pppppppbVar9,(int)local_40);
      local_8._0_1_ = 2;
      uVar3 = (undefined1)local_8;
      local_8._0_1_ = 2;
      if (0xf < local_3c) {
        pppppppbVar9 = local_50[0];
        if ((0xfff < local_3c + 1) &&
           (pppppppbVar9 = (byte *******)local_50[0][-1],
           (byte *)0x1f < (byte *)((int)local_50[0] + (-4 - (int)pppppppbVar9)))) goto LAB_1001958f;
        FUN_10053fdd(pppppppbVar9);
      }
      local_40 = (undefined4 *)0x0;
      local_3c = 0xf;
      local_50[0] = (byte *******)((uint)local_50[0] & 0xffffff00);
      local_8._0_1_ = 4;
      pwVar4 = (wchar_t *)local_38;
      if (0xf < local_24) {
        pwVar4 = (wchar_t *)local_38[0];
      }
      unaff_EDI = local_28;
      FUN_1000c2f0(puVar6 + 0x18,pwVar4,(uint)local_28);
      local_8._0_1_ = 2;
      if (0xf < local_24) {
        unaff_EBX = (wchar_t *)local_38[0];
        if ((0xfff < local_24 + 1) &&
           (unaff_EBX = (wchar_t *)local_38[0][-1], uVar3 = (undefined1)local_8,
           (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)unaff_EBX)))) goto LAB_1001958f;
        unaff_ESI = 
        L"쒃贈ꁍ䗆Ǽ짨I贀낍\xfffe웿ﱅ\xe800믊\xfffe䖋藬࿀龅\xfffe쟿ﱅ\xffff\xffff삅ॴ\xe850㷾\x05쒃耄岿\x02"
        ;
        FUN_10053fdd(unaff_EBX);
      }
      local_8._0_1_ = 1;
      FUN_1001d730(&local_64);
      local_8 = (uint)local_8._1_3_ << 8;
      in_stack_fffffeac = (uint *)0x10018d76;
      FUN_10004940((int *)&stack0xfffffeac);
    }
  }
  local_8._1_3_ = 0xffffff;
  local_8._0_1_ = 0xff;
  if (*(char *)(param_1 + 0x97) != '\0') goto LAB_1001955d;
  puVar6 = (undefined4 *)0x10018db8;
  ppuVar7 = (uint **)FUN_1003def0(0x483,0x5740,(int *)&local_68);
  puVar2 = local_68;
  if (ppuVar7 == (uint **)0x0) {
    local_5c = local_68;
    local_8._0_1_ = 5;
    local_8._1_3_ = 0;
    if (local_68 == (uint *)0x0) {
      if (*(byte *)(param_1 + 3) < 5) {
        local_6c = &local_20;
        local_1c = (uint **)0x0;
        pppppppuVar19 = &local_6c;
        pppuVar16 = &local_1c;
        local_20 = (undefined4 *******)0x1;
        pvVar5 = (void *)FUN_1005f320();
        FUN_10020d90(pvVar5,pppuVar16,pppppppuVar19);
        local_8._0_1_ = 0x17;
        while (local_1c != (uint **)0x0) {
          FUN_10007bd0((int *)&stack0xfffffeac);
          local_8._0_1_ = 0x18;
          local_78 = FUN_1005f320();
          puVar10 = FUN_100573c0(&local_1c);
          local_74 = puVar10;
          local_70 = ___uncaught_exceptions();
          piVar15 = local_144;
          local_8 = CONCAT31(local_8._1_3_,0x19);
          pcVar17 = "Device not connected";
          uVar13 = 0x100193d8;
          FUN_1000b420(piVar15,"Device not connected");
          if (puVar10 == (undefined4 *)0x0) {
            unaff_EDI = (uint *)0x216;
            pwVar4 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
            pwVar18 = L"m_pStreamCompound != 0";
            piVar15 = (int *)0x100193f3;
            FID_conflict___assert
                      (L"m_pStreamCompound != 0",
                       L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",
                       0x216);
            pcVar17 = (char *)pwVar18;
          }
          FUN_10007b10(&stack0xfffffeac,&stack0xfffffe8c);
          FUN_10031fd0(local_38,puVar6,uVar13,piVar15,pcVar17,(uint)pwVar4,(uint)unaff_EDI);
          local_8._0_1_ = 0x1a;
          pppppppbVar9 = (byte *******)local_38;
          if (0xf < local_24) {
            pppppppbVar9 = local_38[0];
          }
          FUN_10031d60(local_94,(byte *)pppppppbVar9,(int)local_28);
          local_8._0_1_ = 0x19;
          if (0xf < local_24) {
            pppppppbVar9 = local_38[0];
            if ((0xfff < local_24 + 1) &&
               (pppppppbVar9 = (byte *******)local_38[0][-1], uVar3 = (undefined1)local_8,
               (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)pppppppbVar9))))
            goto LAB_1001958f;
            FUN_10053fdd(pppppppbVar9);
          }
          local_28 = (uint *)0x0;
          local_24 = 0xf;
          local_38[0] = (byte *******)((uint)local_38[0] & 0xffffff00);
          local_8._0_1_ = 0x1b;
          pwVar4 = (wchar_t *)local_94;
          if (0xf < local_80) {
            pwVar4 = (wchar_t *)local_94[0];
          }
          unaff_EDI = local_84;
          FUN_1000c2f0(puVar10 + 0x18,pwVar4,(uint)local_84);
          local_8._0_1_ = 0x19;
          if (0xf < local_80) {
            pppppppbVar9 = local_94[0];
            if ((0xfff < local_80 + 1) &&
               (pppppppbVar9 = (byte *******)local_94[0][-1], uVar3 = (undefined1)local_8,
               (byte *)0x1f < (byte *)((int)local_94[0] + (-4 - (int)pppppppbVar9))))
            goto LAB_1001958f;
            FUN_10053fdd(pppppppbVar9);
          }
          local_8._0_1_ = 0x18;
          FUN_1001d730(&local_78);
          local_8._0_1_ = 0x17;
          FUN_10004940((int *)&stack0xfffffeac);
        }
        local_8._0_1_ = 5;
        puVar12 = (uint *)param_1[1];
        puVar11 = (uint *)*param_1;
        local_20 = (undefined4 *******)0x54;
        if (puVar11 != puVar12) {
          do {
            if (*puVar11 == 0x54) break;
            puVar11 = puVar11 + 1;
          } while (puVar11 != puVar12);
          if (puVar11 != puVar12) goto LAB_10019552;
        }
        if ((uint *)param_1[2] == puVar12) {
          FUN_10021980(param_1,puVar12,(uint *)&local_20);
        }
        else {
          *puVar12 = 0x54;
          param_1[1] = param_1[1] + 4;
        }
      }
    }
    else {
      local_8._0_1_ = 6;
      local_8._1_3_ = 0;
      pwVar18 = 
      L"쒃蔐࿀膅\a贀鱅䗆߼ｐ\xe875壨ɜ茀ࣄ삅ᡴ赐悍\xffff\xe8ff夅\xffff쁨ྚ謐\xe9c1ݢ"
      ;
      puVar12 = local_68;
      local_1c = ppuVar7;
      ppuVar7 = (uint **)FUN_1003e7e0(local_68,0,0,&local_1c);
      if (ppuVar7 != (uint **)0x0) goto LAB_10019579;
      local_8._0_1_ = 7;
      iVar8 = FUN_1003ea60((int)local_1c,&local_68);
      if (iVar8 != 0) {
        FUN_1000e720(local_a4,iVar8);
        piVar15 = extraout_ECX;
        goto LAB_10019589;
      }
      local_40 = (undefined4 *)0x0;
      local_3c = 0xf;
      local_50[0] = (byte *******)((uint)local_50[0] & 0xffffff00);
      puVar11 = local_68;
      do {
        uVar1 = *puVar11;
        puVar11 = (uint *)((int)puVar11 + 1);
      } while ((char)uVar1 != '\0');
      FUN_100030d0(local_50,local_68,(int)puVar11 - ((int)local_68 + 1));
      thunk_FUN_100a054e(local_68);
      local_8._0_1_ = 8;
      if (*(byte *)(param_1 + 3) < 5) {
        local_20 = &local_6c;
        local_18 = (void *)0x0;
        pppppppuVar19 = &local_20;
        ppvVar14 = &local_18;
        local_6c = (undefined4 *******)0x1;
        pvVar5 = (void *)FUN_1005f320();
        FUN_10020d90(pvVar5,ppvVar14,pppppppuVar19);
        local_8._0_1_ = 9;
        while (local_18 != (void *)0x0) {
          FUN_10007bd0((int *)&stack0xfffffeac);
          local_8._0_1_ = 10;
          local_78 = FUN_1005f320();
          puVar6 = FUN_100573c0(&local_18);
          local_74 = puVar6;
          local_70 = ___uncaught_exceptions();
          local_8 = CONCAT31(local_8._1_3_,0xb);
          FUN_1000b420(local_144,"device = ");
          pppppppbVar9 = (byte *******)local_50;
          if (0xf < local_3c) {
            pppppppbVar9 = local_50[0];
          }
          puVar12 = (uint *)0x10018f13;
          puVar10 = local_40;
          FUN_1000c2f0(local_144,pppppppbVar9,(uint)local_40);
          if (puVar6 == (undefined4 *)0x0) {
            in_stack_fffffeac = (uint *)0x216;
            unaff_EBX = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
            unaff_ESI = L"m_pStreamCompound != 0";
            unaff_EDI = (uint *)0x10018f2e;
            FID_conflict___assert
                      (L"m_pStreamCompound != 0",
                       L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",
                       0x216);
          }
          pwVar20 = (wchar_t *)(puVar6 + 0x18);
          FUN_10007b10(&stack0xfffffeac,&stack0xfffffe98);
          FUN_10031fd0(local_38,puVar10,pwVar4,unaff_EDI,unaff_ESI,(uint)unaff_EBX,
                       (uint)in_stack_fffffeac);
          local_8._0_1_ = 0xc;
          pppppppbVar9 = (byte *******)local_38;
          if (0xf < local_24) {
            pppppppbVar9 = local_38[0];
          }
          FUN_10031d60(local_94,(byte *)pppppppbVar9,(int)local_28);
          local_8._0_1_ = 0xb;
          if (0xf < local_24) {
            pppppppbVar9 = local_38[0];
            if ((0xfff < local_24 + 1) &&
               (pppppppbVar9 = (byte *******)local_38[0][-1], uVar3 = (undefined1)local_8,
               (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)pppppppbVar9))))
            goto LAB_1001958f;
            FUN_10053fdd(pppppppbVar9);
          }
          local_28 = (uint *)0x0;
          local_24 = 0xf;
          local_38[0] = (byte *******)((uint)local_38[0] & 0xffffff00);
          local_8._0_1_ = 0xd;
          unaff_EBX = (wchar_t *)local_94;
          if (0xf < local_80) {
            unaff_EBX = (wchar_t *)local_94[0];
          }
          unaff_EDI = (uint *)0x10018fd4;
          in_stack_fffffeac = local_84;
          FUN_1000c2f0((int *)pwVar20,unaff_EBX,(uint)local_84);
          local_8._0_1_ = 0xb;
          if (0xf < local_80) {
            pppppppbVar9 = local_94[0];
            if ((0xfff < local_80 + 1) &&
               (pppppppbVar9 = (byte *******)local_94[0][-1], uVar3 = (undefined1)local_8,
               (byte *)0x1f < (byte *)((int)local_94[0] + (-4 - (int)pppppppbVar9))))
            goto LAB_1001958f;
            FUN_10053fdd(pppppppbVar9);
          }
          local_8._0_1_ = 10;
          FUN_1001d730(&local_78);
          local_8._0_1_ = 9;
          FUN_10004940((int *)&stack0xfffffeac);
          unaff_ESI = pwVar20;
        }
      }
      local_8._0_1_ = 8;
      if (param_1[0x65] == -1) {
        FUN_10039a40(param_1 + 0x62,(uint *)local_50);
        PurgeComm((HANDLE)param_1[0x65],0xf);
        puVar6 = FUN_1000e6f0(&local_64,1);
        param_1[0x74] = *puVar6;
        param_1[0x75] = puVar6[1];
        if (0xf < local_3c) {
          pppppppbVar9 = local_50[0];
          if ((0xfff < local_3c + 1) &&
             (pppppppbVar9 = (byte *******)local_50[0][-1], uVar3 = (undefined1)local_8,
             (byte *)0x1f < (byte *)((int)local_50[0] + (-4 - (int)pppppppbVar9)))) {
LAB_1001958f:
            local_8._0_1_ = uVar3;
                    /* WARNING: Subroutine does not return */
            FUN_1009cac3();
          }
          FUN_10053fdd(pppppppbVar9);
        }
        local_40 = (undefined4 *)0x0;
        local_3c = 0xf;
        local_50[0] = (byte *******)((uint)local_50[0] & 0xffffff00);
        FUN_1003ea30(local_1c);
        goto LAB_10019552;
      }
      if (*(byte *)(param_1 + 3) < 5) {
        local_6c = &local_20;
        local_18 = (void *)0x0;
        pppppppuVar19 = &local_6c;
        ppvVar14 = &local_18;
        local_20 = (undefined4 *******)0x1;
        pvVar5 = (void *)FUN_1005f320();
        FUN_10020d90(pvVar5,ppvVar14,pppppppuVar19);
        local_8._0_1_ = 0x12;
        while (local_18 != (void *)0x0) {
          FUN_10007bd0((int *)&stack0xfffffeac);
          local_8._0_1_ = 0x13;
          local_78 = FUN_1005f320();
          puVar6 = FUN_100573c0(&local_18);
          local_74 = puVar6;
          local_70 = ___uncaught_exceptions();
          piVar15 = local_144;
          local_8 = CONCAT31(local_8._1_3_,0x14);
          pcVar17 = "Device in use";
          uVar13 = 0x10019178;
          FUN_1000b420(piVar15,"Device in use");
          if (puVar6 == (undefined4 *)0x0) {
            puVar12 = (uint *)0x216;
            pwVar18 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
            pwVar4 = L"m_pStreamCompound != 0";
            piVar15 = (int *)0x10019193;
            FID_conflict___assert
                      (L"m_pStreamCompound != 0",
                       L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",
                       0x216);
            pcVar17 = (char *)pwVar4;
          }
          FUN_10007b10(&stack0xfffffeac,&stack0xfffffe78);
          FUN_10031fd0(local_38,in_stack_fffffe78,uVar13,piVar15,pcVar17,(uint)pwVar18,(uint)puVar12
                      );
          local_8._0_1_ = 0x15;
          pppppppbVar9 = (byte *******)local_38;
          if (0xf < local_24) {
            pppppppbVar9 = local_38[0];
          }
          FUN_10031d60(local_94,(byte *)pppppppbVar9,(int)local_28);
          local_8._0_1_ = 0x14;
          if (0xf < local_24) {
            pppppppbVar9 = local_38[0];
            if ((0xfff < local_24 + 1) &&
               (pppppppbVar9 = (byte *******)local_38[0][-1], uVar3 = (undefined1)local_8,
               (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)pppppppbVar9))))
            goto LAB_1001958f;
            FUN_10053fdd(pppppppbVar9);
          }
          local_28 = (uint *)0x0;
          local_24 = 0xf;
          local_38[0] = (byte *******)((uint)local_38[0] & 0xffffff00);
          local_8._0_1_ = 0x16;
          pwVar18 = (wchar_t *)local_94;
          if (0xf < local_80) {
            pwVar18 = (wchar_t *)local_94[0];
          }
          puVar12 = local_84;
          FUN_1000c2f0(puVar6 + 0x18,pwVar18,(uint)local_84);
          local_8._0_1_ = 0x14;
          if (0xf < local_80) {
            pppppppbVar9 = local_94[0];
            if ((0xfff < local_80 + 1) &&
               (pppppppbVar9 = (byte *******)local_94[0][-1], uVar3 = (undefined1)local_8,
               (byte *)0x1f < (byte *)((int)local_94[0] + (-4 - (int)pppppppbVar9))))
            goto LAB_1001958f;
            FUN_10053fdd(pppppppbVar9);
          }
          local_8._0_1_ = 0x13;
          FUN_1001d730(&local_78);
          local_8._0_1_ = 0x12;
          FUN_10004940((int *)&stack0xfffffeac);
        }
        local_8._0_1_ = 8;
        puVar12 = (uint *)param_1[1];
        puVar11 = (uint *)*param_1;
        local_20 = (undefined4 *******)0x53;
        if (puVar11 != puVar12) {
          do {
            if (*puVar11 == 0x53) break;
            puVar11 = puVar11 + 1;
          } while (puVar11 != puVar12);
          if (puVar11 != puVar12) goto LAB_100192ed;
        }
        if ((uint *)param_1[2] == puVar12) {
          FUN_10021980(param_1,puVar12,(uint *)&local_20);
        }
        else {
          *puVar12 = 0x53;
          param_1[1] = param_1[1] + 4;
        }
      }
LAB_100192ed:
      if (0xf < local_3c) {
        pppppppbVar9 = local_50[0];
        if ((0xfff < local_3c + 1) &&
           (pppppppbVar9 = (byte *******)local_50[0][-1],
           (byte *)0x1f < (byte *)((int)local_50[0] + (-4 - (int)pppppppbVar9)))) {
                    /* WARNING: Subroutine does not return */
          FUN_1009cac3();
        }
        FUN_10053fdd(pppppppbVar9);
      }
      local_40 = (undefined4 *)0x0;
      local_3c = 0xf;
      local_50[0] = (byte *******)((uint)local_50[0] & 0xffffff00);
      FUN_1003ea30(local_1c);
    }
LAB_10019552:
    FUN_1003e6c0(puVar2);
LAB_1001955d:
    ExceptionList = local_10;
    __security_check_cookie((uint)local_14 ^ (uint)&stack0xfffffffc);
    return;
  }
LAB_10019579:
  FUN_1000e720(local_7c,ppuVar7);
  piVar15 = extraout_ECX_00;
LAB_10019589:
                    /* WARNING: Subroutine does not return */
  __CxxThrowException_8(piVar15,&DAT_100f9ac0);
}


```


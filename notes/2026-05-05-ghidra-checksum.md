## checksum FUN_100340c0 @ 0x100340c0

```c

undefined4 __fastcall FUN_100340c0(int param_1,uint param_2)

{
  byte *pbVar1;
  ulonglong uVar2;
  undefined1 auVar3 [15];
  undefined1 auVar4 [15];
  undefined1 auVar5 [15];
  undefined1 auVar6 [15];
  undefined1 auVar7 [15];
  undefined1 auVar8 [15];
  undefined1 auVar9 [15];
  undefined1 auVar10 [15];
  undefined1 auVar11 [15];
  undefined1 auVar12 [15];
  undefined1 auVar13 [15];
  undefined1 auVar14 [15];
  undefined1 auVar15 [15];
  unkuint9 Var16;
  undefined1 auVar17 [11];
  undefined1 auVar18 [13];
  undefined1 auVar19 [15];
  undefined1 auVar20 [11];
  undefined1 auVar21 [13];
  undefined1 auVar22 [15];
  undefined1 auVar23 [15];
  undefined1 auVar24 [15];
  undefined1 auVar25 [15];
  int iVar26;
  ushort uVar27;
  uint uVar28;
  short sVar29;
  short sVar30;
  short sVar31;
  short sVar32;
  short sVar33;
  short sVar34;
  short sVar35;
  short sVar36;
  short sVar37;
  short sVar38;
  short sVar39;
  short sVar40;
  short sVar41;
  short sVar42;
  short sVar43;
  short sVar44;
  undefined4 local_10;
  undefined4 local_c;
  undefined2 local_8;
  
  uVar28 = param_2 & 0xffff;
  local_8 = 0;
  iVar26 = 0;
  if ((uVar28 != 0) && (0xf < uVar28)) {
    sVar37 = 0;
    sVar38 = 0;
    sVar39 = 0;
    sVar40 = 0;
    sVar41 = 0;
    sVar42 = 0;
    sVar43 = 0;
    sVar44 = 0;
    sVar29 = 0;
    sVar30 = 0;
    sVar31 = 0;
    sVar32 = 0;
    sVar33 = 0;
    sVar34 = 0;
    sVar35 = 0;
    sVar36 = 0;
    do {
      uVar2 = *(ulonglong *)(param_1 + iVar26);
      auVar3._8_6_ = 0;
      auVar3._0_8_ = uVar2;
      auVar3[0xe] = (char)(uVar2 >> 0x38);
      auVar5._8_4_ = 0;
      auVar5._0_8_ = uVar2;
      auVar5[0xc] = (char)(uVar2 >> 0x30);
      auVar5._13_2_ = auVar3._13_2_;
      auVar7._8_4_ = 0;
      auVar7._0_8_ = uVar2;
      auVar7._12_3_ = auVar5._12_3_;
      auVar9._8_2_ = 0;
      auVar9._0_8_ = uVar2;
      auVar9[10] = (char)(uVar2 >> 0x28);
      auVar9._11_4_ = auVar7._11_4_;
      auVar11._8_2_ = 0;
      auVar11._0_8_ = uVar2;
      auVar11._10_5_ = auVar9._10_5_;
      auVar13[8] = (char)(uVar2 >> 0x20);
      auVar13._0_8_ = uVar2;
      auVar13._9_6_ = auVar11._9_6_;
      auVar15._7_8_ = 0;
      auVar15._0_7_ = auVar13._8_7_;
      Var16 = CONCAT81(SUB158(auVar15 << 0x40,7),(char)(uVar2 >> 0x18));
      auVar22._9_6_ = 0;
      auVar22._0_9_ = Var16;
      auVar17._1_10_ = SUB1510(auVar22 << 0x30,5);
      auVar17[0] = (char)(uVar2 >> 0x10);
      auVar23._11_4_ = 0;
      auVar23._0_11_ = auVar17;
      auVar18._1_12_ = SUB1512(auVar23 << 0x20,3);
      auVar18[0] = (char)(uVar2 >> 8);
      sVar37 = sVar37 + (ushort)(byte)uVar2;
      sVar38 = sVar38 + auVar18._0_2_;
      sVar39 = sVar39 + auVar17._0_2_;
      sVar40 = sVar40 + (short)Var16;
      sVar41 = sVar41 + auVar13._8_2_;
      sVar42 = sVar42 + auVar9._10_2_;
      sVar43 = sVar43 + auVar5._12_2_;
      sVar44 = sVar44 + (auVar3._13_2_ >> 8);
      uVar2 = *(ulonglong *)(param_1 + 8 + iVar26);
      iVar26 = iVar26 + 0x10;
      auVar4._8_6_ = 0;
      auVar4._0_8_ = uVar2;
      auVar4[0xe] = (char)(uVar2 >> 0x38);
      auVar6._8_4_ = 0;
      auVar6._0_8_ = uVar2;
      auVar6[0xc] = (char)(uVar2 >> 0x30);
      auVar6._13_2_ = auVar4._13_2_;
      auVar8._8_4_ = 0;
      auVar8._0_8_ = uVar2;
      auVar8._12_3_ = auVar6._12_3_;
      auVar10._8_2_ = 0;
      auVar10._0_8_ = uVar2;
      auVar10[10] = (char)(uVar2 >> 0x28);
      auVar10._11_4_ = auVar8._11_4_;
      auVar12._8_2_ = 0;
      auVar12._0_8_ = uVar2;
      auVar12._10_5_ = auVar10._10_5_;
      auVar14[8] = (char)(uVar2 >> 0x20);
      auVar14._0_8_ = uVar2;
      auVar14._9_6_ = auVar12._9_6_;
      auVar19._7_8_ = 0;
      auVar19._0_7_ = auVar14._8_7_;
      Var16 = CONCAT81(SUB158(auVar19 << 0x40,7),(char)(uVar2 >> 0x18));
      auVar24._9_6_ = 0;
      auVar24._0_9_ = Var16;
      auVar20._1_10_ = SUB1510(auVar24 << 0x30,5);
      auVar20[0] = (char)(uVar2 >> 0x10);
      auVar25._11_4_ = 0;
      auVar25._0_11_ = auVar20;
      auVar21._1_12_ = SUB1512(auVar25 << 0x20,3);
      auVar21[0] = (char)(uVar2 >> 8);
      sVar29 = sVar29 + (ushort)(byte)uVar2;
      sVar30 = sVar30 + auVar21._0_2_;
      sVar31 = sVar31 + auVar20._0_2_;
      sVar32 = sVar32 + (short)Var16;
      sVar33 = sVar33 + auVar14._8_2_;
      sVar34 = sVar34 + auVar10._10_2_;
      sVar35 = sVar35 + auVar6._12_2_;
      sVar36 = sVar36 + (auVar4._13_2_ >> 8);
    } while (iVar26 < (int)(param_2 & 0xfff0));
    local_8 = sVar29 + sVar37 + sVar33 + sVar41 + sVar31 + sVar39 + sVar35 + sVar43 +
              sVar30 + sVar38 + sVar34 + sVar42 + sVar32 + sVar40 + sVar36 + sVar44;
  }
  local_10 = 0;
  local_c = 0;
  if (iVar26 < (int)uVar28) {
    if (1 < (int)(uVar28 - iVar26)) {
      uVar27 = 0;
      local_10._0_2_ = 0;
      do {
        local_10._0_2_ = (ushort)local_10 + *(byte *)(param_1 + iVar26);
        pbVar1 = (byte *)(param_1 + 1 + iVar26);
        iVar26 = iVar26 + 2;
        uVar27 = uVar27 + *pbVar1;
      } while (iVar26 < (int)(uVar28 - 1));
      local_c = (uint)uVar27;
      local_10 = (uint)(ushort)local_10;
    }
    if (iVar26 < (int)uVar28) {
      local_8 = local_8 + (ushort)*(byte *)(iVar26 + param_1);
    }
    iVar26 = local_c + local_10;
    local_8 = local_8 + (short)iVar26;
  }
  return CONCAT22((short)((uint)iVar26 >> 0x10),local_8);
}


```

## read_bytes FUN_10039cb0 @ 0x10039cb0

```c

void __thiscall FUN_10039cb0(void *this,int param_1,uint param_2)

{
  int *this_00;
  uint *puVar1;
  int iVar2;
  uint *this_01;
  undefined4 *puVar3;
  void *pvVar4;
  uint uVar5;
  int local_e4 [11];
  char local_b8;
  void *local_b4 [2];
  basic_string<char,struct_std::char_traits<char>,class_std::allocator<char>_> local_ac [8];
  undefined4 local_a4;
  uint local_a0;
  int local_9c;
  uint local_98;
  int local_94;
  code *local_90;
  void *local_8c;
  undefined4 local_80;
  uint local_7c;
  int local_78;
  undefined *local_74 [2];
  undefined8 local_6c;
  undefined4 local_60;
  undefined **local_5c [18];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_100c544c;
  local_10 = ExceptionList;
  local_14 = DAT_100fc0f4 ^ (uint)&stack0xfffffffc;
  ExceptionList = &local_10;
  local_7c = 0;
  local_78 = param_1;
  if (**(int **)((int)this + 0x70) == **(int **)((int)this + 0x6c)) {
    local_7c = param_2;
  }
  else {
    _memset(local_74,0,0x60);
    local_74[0] = &DAT_100e04b8;
    local_8 = 0;
    local_7c = 1;
    local_5c[0] = std::basic_istream<char,struct_std::char_traits<char>_>::vftable;
    local_60 = 0;
    local_6c = 0;
    FUN_1000b090(local_5c,(int)this + 0x50,'\0');
    local_8 = 1;
    uVar5 = **(int **)((int)this + 0x70) - **(int **)((int)this + 0x6c);
    if (param_2 < uVar5) {
      uVar5 = param_2;
    }
    FUN_1003b0a0(local_74,local_78,uVar5,0);
    local_78 = local_78 + uVar5;
    local_7c = param_2 - uVar5;
    *(undefined ***)((int)local_74 + *(int *)(local_74[0] + 4)) =
         std::basic_istream<char,struct_std::char_traits<char>_>::vftable;
    *(int *)((int)local_74 + *(int *)(local_74[0] + 4) + -4) = *(int *)(local_74[0] + 4) + -0x18;
    if (local_7c == 0) {
      local_8 = 2;
      local_5c[0] = std::ios_base::vftable;
      std::ios_base::_Ios_base_dtor((ios_base *)local_5c);
      goto LAB_10039f1b;
    }
    local_8 = 3;
    local_5c[0] = std::ios_base::vftable;
    std::ios_base::_Ios_base_dtor((ios_base *)local_5c);
  }
  local_8 = 0xffffffff;
  puVar1 = FUN_1000e6f0(&local_94,0);
  this_01 = (uint *)((int)this + 0x48);
  iVar2 = FUN_1003b810(this_01,puVar1);
  this_00 = (int *)((int)this + 0x20);
  if (iVar2 == 0) {
    this_01 = FUN_100391b0(&local_94);
  }
  FUN_1003a580(this_00,this_01);
  local_90 = FUN_1003a1c0;
  local_8c = this;
  FUN_1003bc60(this_00,(ULONG_PTR *)&local_90);
  local_b8 = '\x01';
  local_a4 = 0;
  local_a0 = 0xf;
  local_b4[0] = (void *)((uint)local_b4[0] & 0xffffff00);
  FUN_100030d0(local_b4,(uint *)&DAT_100e0149,0);
  local_9c = local_78;
  local_98 = local_7c;
  *(char *)((int)this + 0xa0) = local_b8;
  FUN_1000afb0((void *)((int)this + 0xa4),(int *)local_b4);
  *(int *)((int)this + 0xbc) = local_9c;
  *(uint *)((int)this + 0xc0) = local_98;
  if (0xf < local_a0) {
    pvVar4 = local_b4[0];
    if ((0xfff < local_a0 + 1) &&
       (pvVar4 = *(void **)((int)local_b4[0] + -4),
       0x1f < (uint)((int)local_b4[0] + (-4 - (int)pvVar4)))) {
                    /* WARNING: Subroutine does not return */
      FUN_1009cac3();
    }
    FUN_10053fdd(pvVar4);
  }
  FUN_1003a090(this,(char *)((int)this + 0xa0));
  *(undefined4 *)((int)this + 0x98) = 0;
  *(undefined4 *)((int)this + 0x9c) = 0;
  while( true ) {
    FUN_10038f00((int)this);
    iVar2 = *(int *)((int)this + 0x98);
    if (iVar2 == 1) break;
    if (iVar2 == 2) {
      FUN_1003a760(this_00);
      FUN_1003a430((int *)((int)this + 0xc));
      puVar3 = FUN_1000d6f0(&local_80);
      FUN_1000db60(local_e4,*puVar3,puVar3[1],"Error while reading");
                    /* WARNING: Subroutine does not return */
      __CxxThrowException_8(local_e4,&DAT_100fa0e4);
    }
    if (iVar2 == 3) {
      FUN_1003a430((int *)((int)this + 0xc));
      std::basic_string<char,struct_std::char_traits<char>,class_std::allocator<char>_>::
      basic_string<char,struct_std::char_traits<char>,class_std::allocator<char>_>
                (local_ac,"Timeout expired");
      local_8 = 4;
      FUN_100398f0(&local_94,(undefined4 *)local_ac);
                    /* WARNING: Subroutine does not return */
      __CxxThrowException_8(&local_94,&DAT_100fa14c);
    }
  }
  FUN_1003a760(this_00);
LAB_10039f1b:
  ExceptionList = local_10;
  __security_check_cookie(local_14 ^ (uint)&stack0xfffffffc);
  return;
}


```


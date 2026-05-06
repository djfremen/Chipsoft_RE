# Init / log-path / JSON parse decompiles

## FUN_10010550 @ 0x10010550

**Strings referenced (max 60):**
- 0x10010a67 → 0x100e0b48  `mdflasher_out.exe`
- 0x10010b4c → 0x100e0b5c  `chiploader.exe`
- 0x10010e7b → 0x100e0b6c  `ALLUSERSPROFILE`

```c

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN_10010550(PRTL_CRITICAL_SECTION_DEBUG param_1)

{
  _LIST_ENTRY **this;
  PRTL_CRITICAL_SECTION_DEBUG p_Var1;
  undefined1 *puVar2;
  short sVar3;
  PRTL_CRITICAL_SECTION_DEBUG p_Var4;
  uint uVar5;
  undefined1 uVar6;
  char cVar7;
  _LIST_ENTRY *p_Var8;
  int *piVar9;
  undefined4 *puVar10;
  DWORD *pDVar11;
  HANDLE pvVar12;
  int iVar13;
  uint *puVar14;
  void **ppvVar15;
  char *pcVar16;
  char *pcVar17;
  undefined4 *****pppppuVar18;
  DWORD DVar19;
  undefined4 extraout_ECX;
  short *psVar20;
  LIST_ENTRY *pLVar21;
  uint *puVar22;
  undefined4 ****ppppuVar23;
  void *pvVar24;
  int iVar25;
  LIST_ENTRY **ppLVar26;
  int iVar27;
  void *local_330 [2];
  void *local_328;
  undefined4 uStack_324;
  undefined4 uStack_320;
  PRTL_CRITICAL_SECTION_DEBUG p_Stack_31c;
  undefined4 local_318;
  void *pvStack_314;
  undefined4 uStack_310;
  undefined4 uStack_30c;
  undefined4 local_308;
  undefined4 ****ppppuStack_304;
  undefined4 uStack_300;
  undefined4 ****ppppuStack_2fc;
  uint local_2f8;
  uint uStack_2f4;
  LIST_ENTRY *pLStack_2f0;
  undefined8 uStack_2ec;
  LIST_ENTRY *local_2e4;
  void *local_2e0;
  undefined4 uStack_2dc;
  undefined4 uStack_2d8;
  PRTL_CRITICAL_SECTION_DEBUG p_Stack_2d4;
  undefined4 local_2d0;
  uint local_2cc;
  PRTL_CRITICAL_SECTION_DEBUG local_2c8;
  LIST_ENTRY local_2c4 [2];
  int local_2b4;
  uint local_2b0;
  LIST_ENTRY local_2ac [2];
  int local_29c;
  uint local_298;
  int local_294 [8];
  void *pvStack_274;
  undefined4 uStack_270;
  undefined4 uStack_26c;
  undefined4 local_268;
  undefined4 ****ppppuStack_264;
  undefined4 uStack_260;
  undefined4 ****ppppuStack_25c;
  undefined4 local_258;
  void *pvStack_254;
  uint uStack_250;
  uint uStack_24c;
  uint local_248;
  undefined8 local_244;
  undefined1 local_23c [16];
  undefined4 local_22c;
  undefined4 local_228;
  LIST_ENTRY *local_224;
  undefined4 local_220;
  uint local_18;
  undefined1 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB_100c2704;
  local_10 = ExceptionList;
  local_18 = DAT_100fc0f4 ^ (uint)&stack0xfffffffc;
  local_14 = &stack0xfffffcbc;
  ExceptionList = &local_10;
  param_1->Type = 0;
  param_1->CreatorBackTraceIndex = 0;
  param_1->CriticalSection = (_RTL_CRITICAL_SECTION *)0x0;
  (param_1->ProcessLocksList).Flink = (_LIST_ENTRY *)0x0;
  local_8 = 0;
  local_2d0 = 0x10000;
  *(undefined8 *)&(param_1->ProcessLocksList).Blink = 0;
  p_Stack_2d4 = _UNK_100e544c;
  uStack_2d8 = _UNK_100e5448;
  uStack_2dc = _UNK_100e5444;
  local_2e0 = _DAT_100e5440;
  param_1->ContentionCount = 0;
  local_2cc = 0x10001;
  p_Stack_31c = param_1;
  local_2c8 = param_1;
  FUN_1001d9f0(&param_1->Flags,&local_2e0,&local_2c8);
  local_8._0_1_ = 1;
  local_328 = _DAT_100e5440;
  uStack_324 = _UNK_100e5444;
  uStack_320 = _UNK_100e5448;
  p_Stack_31c = _UNK_100e544c;
  FUN_1001d9f0(param_1 + 1,&local_328,&local_318);
  local_8._0_1_ = 2;
  pLVar21 = &param_1[1].ProcessLocksList;
  pLStack_2f0 = (LIST_ENTRY *)0x4;
  uStack_2ec = 0x1000000005;
  pLVar21->Flink = (_LIST_ENTRY *)0x0;
  param_1[1].ProcessLocksList.Blink = (_LIST_ENTRY *)0x0;
  local_224 = pLVar21;
  p_Var8 = (_LIST_ENTRY *)FUN_10020520();
  pLVar21->Flink = p_Var8;
  local_8._0_1_ = 3;
  ppLVar26 = &pLStack_2f0;
  do {
    p_Var8 = pLVar21->Flink;
    piVar9 = (int *)FUN_10026b80(local_224,ppLVar26);
    pLVar21 = local_224;
    FUN_10026ba0(local_224,&p_Stack_31c,(int *)p_Var8,piVar9 + 4,piVar9);
    p_Var4 = local_2c8;
    ppLVar26 = ppLVar26 + 1;
  } while (ppLVar26 != &local_2e4);
  local_8._0_1_ = 4;
  local_248 = 0x8009;
  local_258 = _DAT_100e5430;
  pvStack_254 = _UNK_100e5434;
  uStack_250 = _UNK_100e5438;
  uStack_24c = _UNK_100e543c;
  local_244 = 0x1000100010000;
  FUN_1001d9f0(&local_2c8[1].EntryCount,&local_258,(undefined4 *)local_23c);
  local_8._0_1_ = 5;
  local_318 = _DAT_100e5430;
  pvStack_314 = _UNK_100e5434;
  uStack_310 = _UNK_100e5438;
  uStack_30c = _UNK_100e543c;
  local_308 = _DAT_100e5450;
  ppppuStack_304 = _UNK_100e5454;
  uStack_300 = _UNK_100e5458;
  ppppuStack_2fc = _UNK_100e545c;
  local_2f8 = _DAT_100e5470;
  uStack_2f4 = _UNK_100e5474;
  pLStack_2f0 = _UNK_100e5478;
  uStack_2ec = CONCAT44(0x10001,_UNK_100e547c);
  FUN_1001d9f0(&p_Var4[1].Flags,&local_318,&local_2e4);
  local_8._0_1_ = 6;
  local_294[7] = _DAT_100e5430;
  pvStack_274 = _UNK_100e5434;
  uStack_270 = _UNK_100e5438;
  uStack_26c = _UNK_100e543c;
  local_268 = _DAT_100e5450;
  ppppuStack_264 = _UNK_100e5454;
  uStack_260 = _UNK_100e5458;
  ppppuStack_25c = _UNK_100e545c;
  local_258 = _DAT_100e5460;
  pvStack_254 = _UNK_100e5464;
  uStack_250 = _UNK_100e5468;
  uStack_24c = _UNK_100e546c;
  local_248 = 0x8010;
  local_244 = 0x1000100010000;
  FUN_1001d9f0(p_Var4 + 2,local_294 + 7,(undefined4 *)local_23c);
  local_8._0_1_ = 7;
  pLVar21 = &p_Var4[2].ProcessLocksList;
  pLVar21->Flink = (_LIST_ENTRY *)0x0;
  p_Var4[2].ProcessLocksList.Blink = (_LIST_ENTRY *)0x0;
  p_Stack_31c = (PRTL_CRITICAL_SECTION_DEBUG)pLVar21;
  p_Var8 = (_LIST_ENTRY *)FUN_10020500();
  pLVar21->Flink = p_Var8;
  __Mtx_init_in_situ(&p_Var4[2].EntryCount,2);
  __Mtx_init_in_situ((undefined4 *)(p_Var4 + 4),2);
  __Mtx_init_in_situ(&p_Var4[5].EntryCount,2);
  __Mtx_init_in_situ((undefined4 *)(p_Var4 + 7),2);
  Concurrency::details::create_stl_condition_variable
            ((stl_condition_variable_interface *)&p_Var4[8].EntryCount);
  Concurrency::details::create_stl_condition_variable
            ((stl_condition_variable_interface *)&p_Var4[9].Flags);
  local_8._0_1_ = 0xe;
  p_Var1 = p_Var4 + 0xb;
  p_Var1->Type = 0;
  p_Var1->CreatorBackTraceIndex = 0;
  p_Var4[0xb].CriticalSection = (_RTL_CRITICAL_SECTION *)0x0;
  p_Var4[0xb].ProcessLocksList.Flink = (_LIST_ENTRY *)0x0;
  p_Var4[0xb].ProcessLocksList.Blink = (_LIST_ENTRY *)0x0;
  p_Var4[0xb].EntryCount = 0;
  p_Stack_31c = p_Var1;
  puVar10 = (undefined4 *)FUN_10053c4a(8);
  *(undefined4 **)p_Var1 = puVar10;
  *puVar10 = 0;
  puVar10[1] = 0;
  **(undefined4 **)p_Var1 = p_Var1;
  local_8._0_1_ = 0xf;
  *(undefined1 *)&p_Var4[0xb].ContentionCount = 0;
  p_Var4[0xb].Flags = 0;
  p_Var4[0xb].CreatorBackTraceIndexHigh = 0;
  p_Var4[0xb].SpareWORD = 0;
  p_Var4[0xc].Type = 0;
  p_Var4[0xc].CreatorBackTraceIndex = 0;
  p_Var4[0xc].CriticalSection = (_RTL_CRITICAL_SECTION *)0x0;
  pLVar21 = &p_Var4[0xc].ProcessLocksList;
  p_Stack_31c = (PRTL_CRITICAL_SECTION_DEBUG)pLVar21;
  FUN_1001dd50('\x01');
  local_8._0_1_ = 0x10;
  local_2e4 = (LIST_ENTRY *)FUN_10053c4a(0x20);
  local_8._0_1_ = 0x11;
  local_2e4->Flink = (_LIST_ENTRY *)0x0;
  local_2e4->Blink = (_LIST_ENTRY *)0x0;
  local_2e4[1].Flink = (_LIST_ENTRY *)0x0;
  local_2e4[1].Blink = (_LIST_ENTRY *)0x0;
  local_2e4[2].Flink = (_LIST_ENTRY *)0x0;
  local_2e4[2].Blink = (_LIST_ENTRY *)0x0;
  local_2e4[3].Flink = (_LIST_ENTRY *)0x0;
  local_2e4[3].Blink = (_LIST_ENTRY *)0x0;
  p_Var8 = (_LIST_ENTRY *)
           FUN_1003b960(local_2e4,(PRTL_CRITICAL_SECTION_DEBUG)pLVar21,extraout_ECX,0xffffffff);
  p_Var4[0xc].ProcessLocksList.Blink = p_Var8;
  p_Var4[0xc].EntryCount = (DWORD)p_Var8[3].Blink;
  local_8._0_1_ = 0x12;
  FUN_1003a500(&p_Var4[0xc].ContentionCount,(int)pLVar21);
  local_8._0_1_ = 0x13;
  local_2e4 = &p_Var4[0xd].ProcessLocksList;
  p_Var8 = (_LIST_ENTRY *)FUN_1003d180(p_Var4[0xc].ProcessLocksList.Blink);
  p_Var4[0xd].ProcessLocksList.Flink = p_Var8;
  pDVar11 = &p_Var4[0xd].EntryCount;
  local_224 = (LIST_ENTRY *)pDVar11;
  FUN_10039170(pDVar11);
  p_Var4[0xd].CreatorBackTraceIndexHigh = 0;
  p_Var4[0xd].SpareWORD = 0;
  p_Var4[0xe].Type = 0;
  p_Var4[0xe].CreatorBackTraceIndex = 0;
  p_Var4[0xe].ProcessLocksList.Flink = (_LIST_ENTRY *)0x0;
  p_Var4[0xe].ProcessLocksList.Blink = (_LIST_ENTRY *)0x0;
  local_8._0_1_ = 0x14;
  FUN_1003b7b0(pDVar11);
  local_8._0_1_ = 0x15;
  pDVar11 = FUN_1000e6f0(&uStack_2ec,0);
  p_Var4[0xe].EntryCount = *pDVar11;
  p_Var4[0xe].ContentionCount = pDVar11[1];
  FUN_1003a360(&p_Var4[0xe].Flags,0xffffffff);
  local_8._0_1_ = 0x16;
  local_2e4 = &p_Var4[0x11].ProcessLocksList;
  p_Var4[0x11].Type = 0;
  p_Var4[0x11].CreatorBackTraceIndex = 0;
  this = &p_Var4[0x11].ProcessLocksList.Blink;
  p_Var4[0x11].CriticalSection = (_RTL_CRITICAL_SECTION *)0x0;
  *(undefined1 *)&local_2e4->Flink = 0;
  p_Var4[0x11].CreatorBackTraceIndexHigh = 0;
  p_Var4[0x11].SpareWORD = 0;
  p_Var4[0x12].Type = 0xf;
  p_Var4[0x12].CreatorBackTraceIndex = 0;
  *(undefined1 *)this = 0;
  FUN_100030d0(this,(uint *)&DAT_100e0149,0);
  p_Var1 = local_2c8;
  p_Var4[0x12].CriticalSection = (_RTL_CRITICAL_SECTION *)0x0;
  p_Var4[0x12].ProcessLocksList.Flink = (_LIST_ENTRY *)0x0;
  local_2c8[0x12].EntryCount = 0;
  local_2c8[0x12].ContentionCount = 0;
  local_2c8[0x12].Flags = 0;
  local_2c8[0x13].Type = 0;
  local_2c8[0x13].CreatorBackTraceIndex = 0;
  local_2c8[0x13].CriticalSection = (_RTL_CRITICAL_SECTION *)0x0;
  pvVar24 = ThreadLocalStoragePointer;
  iVar25 = _tls_index;
  local_8._0_1_ = 0x19;
  uVar6 = (undefined1)local_8;
  local_8._0_1_ = 0x19;
  local_2c8[0x13].ProcessLocksList.Flink = (_LIST_ENTRY *)0x0;
  local_2c8[0x13].ProcessLocksList.Blink = (_LIST_ENTRY *)0x0;
  *(undefined2 *)&local_2c8[0x13].EntryCount = 0;
  iVar25 = *(int *)((int)pvVar24 + iVar25 * 4);
  *(undefined1 *)((int)&local_2c8[0x13].EntryCount + 2) = 0;
  if ((*(int *)(iVar25 + 4) < DAT_1010ae18) &&
     (FUN_10054190(&DAT_1010ae18), uVar6 = (undefined1)local_8, DAT_1010ae18 == -1)) {
    local_8._0_1_ = 0x1a;
    _DAT_10107dc8 = 0;
    _DAT_10107dc0 = 0;
    local_22c = 0;
    local_228 = 0xf;
    local_23c[0] = 0;
    FUN_100030d0(local_23c,(uint *)"mdflasher_out.exe",0x11);
    local_8._0_1_ = 0x1b;
    _DAT_10107dc0 = 0;
    _DAT_10107dc8 = 0;
    FUN_10021820(&DAT_10107dc0,(uint *)local_23c,(uint *)&local_224);
    local_8._0_1_ = 0x1a;
    _eh_vector_destructor_iterator_(local_23c,0x18,1,FUN_10002f70);
    _atexit((_func_4879 *)&LAB_100cbc50);
    local_8._0_1_ = 0x19;
    FUN_10054146(&DAT_1010ae18);
    uVar6 = (undefined1)local_8;
  }
  local_8._0_1_ = uVar6;
  if ((*(int *)(iVar25 + 4) < DAT_10107dcc) && (FUN_10054190(&DAT_10107dcc), DAT_10107dcc == -1)) {
    local_8._0_1_ = 0x1c;
    _DAT_10107de8 = 0;
    _DAT_10107de0 = 0;
    local_22c = 0;
    local_228 = 0xf;
    local_23c[0] = 0;
    FUN_100030d0(local_23c,(uint *)"chiploader.exe",0xe);
    local_8._0_1_ = 0x1d;
    _DAT_10107de0 = 0;
    _DAT_10107de8 = 0;
    FUN_10021820(&DAT_10107de0,(uint *)local_23c,(uint *)&local_224);
    local_8._0_1_ = 0x1c;
    _eh_vector_destructor_iterator_(local_23c,0x18,1,FUN_10002f70);
    _atexit((_func_4879 *)&LAB_100cbc40);
    local_8._0_1_ = 0x19;
    FUN_10054146(&DAT_10107dcc);
  }
  puVar10 = &local_220;
  p_Var1[0x12].CreatorBackTraceIndexHigh = 0;
  pvVar12 = GetCurrentProcess();
  K32GetProcessImageFileNameW(pvVar12,puVar10);
  local_2b4 = 0;
  psVar20 = (short *)&local_220;
  local_2b0 = 7;
  local_2c4[0].Flink = (_LIST_ENTRY *)((uint)local_2c4[0].Flink._2_2_ << 0x10);
  do {
    sVar3 = *psVar20;
    psVar20 = psVar20 + 1;
  } while (sVar3 != 0);
  FUN_1001f710(local_2c4,&local_220,(int)psVar20 - ((int)&local_220 + 2) >> 1);
  local_8._0_1_ = 0x1e;
  pLVar21 = local_2c4;
  if (7 < local_2b0) {
    pLVar21 = local_2c4[0].Flink;
  }
  uStack_2ec._0_4_ = 0;
  uStack_2ec._4_4_ = 0xf;
  ppppuStack_2fc = (undefined4 ****)((uint)ppppuStack_2fc & 0xffffff00);
  puVar2 = (undefined1 *)((int)&pLVar21->Flink + local_2b4 * 2);
  local_224 = local_2c4;
  if (7 < local_2b0) {
    local_224 = local_2c4[0].Flink;
  }
  FUN_10003510(&ppppuStack_2fc,(int)puVar2 - (int)local_224 >> 1);
  FUN_10026170(&ppppuStack_2fc,(undefined1 *)local_224,puVar2);
  local_8._0_1_ = 0x1f;
  FUN_10033db0((uint *)local_2ac,(uint *)&ppppuStack_2fc);
  local_8 = CONCAT31(local_8._1_3_,0x21);
  if (0xf < uStack_2ec._4_4_) {
    ppppuVar23 = ppppuStack_2fc;
    if ((0xfff < uStack_2ec._4_4_ + 1) &&
       (ppppuVar23 = (undefined4 ****)ppppuStack_2fc[-1],
       0x1f < (uint)((int)ppppuStack_2fc + (-4 - (int)ppppuVar23)))) {
                    /* WARNING: Subroutine does not return */
      FUN_1009cac3();
    }
    FUN_10053fdd(ppppuVar23);
  }
  local_224 = local_2ac;
  if (0xf < local_298) {
    local_224 = local_2ac[0].Flink;
  }
  pLVar21 = (LIST_ENTRY *)((int)&local_224->Flink + local_29c);
  uStack_2ec = 0xf00000000;
  ppppuStack_2fc = (undefined4 ****)((uint)ppppuStack_2fc & 0xffffff00);
  local_2e4 = local_2ac;
  if (0xf < local_298) {
    local_2e4 = local_2ac[0].Flink;
  }
  iVar27 = (int)pLVar21 - (int)local_2e4;
  iVar25 = 0;
  if (pLVar21 < local_2e4) {
    iVar27 = 0;
  }
  if (iVar27 != 0) {
    do {
      iVar13 = _tolower((int)*(char *)((int)&local_2e4->Flink + iVar25));
      *(char *)((int)&local_224->Flink + iVar25) = (char)iVar13;
      iVar25 = iVar25 + 1;
    } while (iVar25 != iVar27);
  }
  local_224 = (LIST_ENTRY *)0x0;
  FUN_10033e60(&local_224,(byte *)local_2ac,DAT_10107de0,(byte *)DAT_10107de4);
  if (local_224 == DAT_10107de4) {
    local_224 = (LIST_ENTRY *)0x0;
    FUN_10033e60(&local_224,(byte *)local_2ac,DAT_10107dc0,(byte *)DAT_10107dc4);
    local_224 = (LIST_ENTRY *)((local_224 == DAT_10107dc4) + 1);
  }
  else {
    local_224 = (LIST_ENTRY *)0x0;
  }
  p_Var4 = local_2c8;
  if (local_224 == (LIST_ENTRY *)0x0) {
    *(undefined2 *)((int)&(local_2c8->ProcessLocksList).Blink + 1) = 0x101;
    *(undefined1 *)((int)&(local_2c8->ProcessLocksList).Blink + 3) = 1;
  }
  else if (local_224 == (LIST_ENTRY *)0x1) {
    *(undefined2 *)((int)&(local_2c8->ProcessLocksList).Blink + 1) = 0;
    *(undefined1 *)((int)&(local_2c8->ProcessLocksList).Blink + 3) = 0;
  }
  local_294[6] = 0;
  local_294[4] = 0;
  local_294[5] = 0;
  local_294[0] = 0;
  local_294[1] = 0;
  local_294[2] = 0;
  local_294[3] = 0;
  FUN_10020a90((undefined1 *)local_294);
  local_8._0_1_ = 0x22;
  puVar14 = (uint *)FUN_100a6254("ALLUSERSPROFILE");
  local_22c = 0;
  local_228 = 0xf;
  local_23c[0] = 0;
  FUN_100030d0(local_23c,(uint *)&DAT_100e0149,0);
  local_8._0_1_ = 0x23;
  if (puVar14 != (uint *)0x0) {
    uStack_320 = 0;
    p_Stack_31c = (PRTL_CRITICAL_SECTION_DEBUG)0xf;
    local_330[0] = (void *)((uint)local_330[0] & 0xffffff00);
    puVar22 = puVar14;
    do {
      uVar5 = *puVar22;
      puVar22 = (uint *)((int)puVar22 + 1);
    } while ((char)uVar5 != '\0');
    FUN_100030d0(local_330,puVar14,(int)puVar22 - ((int)puVar14 + 1));
    local_8._0_1_ = 0x24;
    puVar14 = FUN_10002e90(local_330,(uint *)&DAT_100e087c);
    ppppuStack_2fc = (undefined4 ****)*puVar14;
    local_2f8 = puVar14[1];
    uStack_2f4 = puVar14[2];
    pLStack_2f0 = (LIST_ENTRY *)puVar14[3];
    uStack_2ec = *(undefined8 *)(puVar14 + 4);
    puVar14[4] = 0;
    puVar14[5] = 0xf;
    *(undefined1 *)puVar14 = 0;
    local_8._0_1_ = 0x25;
    puVar14 = FUN_10020fb0((uint *)&local_2e0,(uint *)&ppppuStack_2fc,&DAT_100fcd38);
    local_8 = CONCAT31(local_8._1_3_,0x26);
    puVar14 = FUN_10002e90(puVar14,(uint *)&DAT_100e087c);
    pvStack_254 = (void *)*puVar14;
    uStack_250 = puVar14[1];
    uStack_24c = puVar14[2];
    local_248 = puVar14[3];
    local_244 = *(undefined8 *)(puVar14 + 4);
    puVar14[4] = 0;
    puVar14[5] = 0xf;
    *(undefined1 *)puVar14 = 0;
    FUN_1000afb0(local_23c,(int *)&pvStack_254);
    if (0xf < local_244._4_4_) {
      pvVar24 = pvStack_254;
      if ((0xfff < local_244._4_4_ + 1) &&
         (pvVar24 = *(void **)((int)pvStack_254 - 4),
         0x1f < (uint)((int)pvStack_254 + (-4 - (int)pvVar24)))) {
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pvVar24);
    }
    local_8._0_1_ = 0x25;
    if (0xf < local_2cc) {
      pvVar24 = local_2e0;
      if ((0xfff < local_2cc + 1) &&
         (pvVar24 = *(void **)((int)local_2e0 + -4),
         0x1f < (uint)((int)local_2e0 + (-4 - (int)pvVar24)))) {
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pvVar24);
    }
    local_8._0_1_ = 0x24;
    uVar6 = (undefined1)local_8;
    local_8._0_1_ = 0x24;
    local_2d0 = 0;
    local_2cc = 0xf;
    local_2e0 = (void *)((uint)local_2e0 & 0xffffff00);
    if (0xf < uStack_2ec._4_4_) {
      ppppuVar23 = ppppuStack_2fc;
      if ((0xfff < uStack_2ec._4_4_ + 1) &&
         (ppppuVar23 = (undefined4 ****)ppppuStack_2fc[-1],
         0x1f < (uint)((int)ppppuStack_2fc + (-4 - (int)ppppuVar23)))) {
        local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(ppppuVar23);
    }
    local_8._0_1_ = 0x23;
    uStack_2ec = 0xf00000000;
    ppppuStack_2fc = (undefined4 ****)((uint)ppppuStack_2fc & 0xffffff00);
    if ((PRTL_CRITICAL_SECTION_DEBUG)0xf < p_Stack_31c) {
      pvVar24 = local_330[0];
      if (((undefined1 *)0xfff < (undefined1 *)((int)&p_Stack_31c->Type + 1)) &&
         (pvVar24 = *(void **)((int)local_330[0] + -4),
         0x1f < (uint)((int)local_330[0] + (-4 - (int)pvVar24)))) {
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pvVar24);
    }
  }
  local_8._0_1_ = 0x28;
  p_Stack_31c = (PRTL_CRITICAL_SECTION_DEBUG)std::locale::_Init(true);
  local_8._0_1_ = 0x29;
  ppvVar15 = (void **)FUN_10020e70(&local_2e0,(uint *)local_23c,&DAT_100fcd68);
  local_8._0_1_ = 0x2a;
  FUN_10021050(ppvVar15,local_294,(int)&uStack_320);
  local_8._0_1_ = 0x29;
  uVar6 = (undefined1)local_8;
  local_8._0_1_ = 0x29;
  if (0xf < local_2cc) {
    pvVar24 = local_2e0;
    if ((0xfff < local_2cc + 1) &&
       (pvVar24 = *(void **)((int)local_2e0 + -4),
       0x1f < (uint)((int)local_2e0 + (-4 - (int)pvVar24)))) {
      local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
      FUN_1009cac3();
    }
    FUN_10053fdd(pvVar24);
  }
  local_2d0 = 0;
  local_2cc = 0xf;
  local_2e0 = (void *)((uint)local_2e0 & 0xffffff00);
  local_8._0_1_ = 0x2b;
  if ((p_Stack_31c != (PRTL_CRITICAL_SECTION_DEBUG)0x0) &&
     (puVar10 = (undefined4 *)(**(code **)(*(int *)p_Stack_31c + 8))(), puVar10 != (undefined4 *)0x0
     )) {
    (**(code **)*puVar10)(1);
  }
  local_8._0_1_ = 0x27;
  FUN_10007a40(&ppppuStack_25c,&DAT_100fccc0);
  local_244 = CONCAT71(local_244._1_7_,0x2e);
  pppppuVar18 = &ppppuStack_25c;
  if (0xf < local_248) {
    pppppuVar18 = (undefined4 *****)ppppuStack_25c;
  }
  local_244 = CONCAT44(pppppuVar18,(undefined4)local_244);
  local_8._0_1_ = 0x2c;
  pcVar16 = (char *)FUN_10025510(local_294,(undefined1 *)&local_2c8,(uint *)&ppppuStack_25c);
  pcVar17 = pcVar16 + 1;
  if (*pcVar16 == '\0') {
    pcVar17 = "\x05";
  }
  local_8._0_1_ = 0x27;
  uVar6 = (undefined1)local_8;
  local_8._0_1_ = 0x27;
  *(char *)&(p_Var4->ProcessLocksList).Blink = *pcVar17;
  if (0xf < local_248) {
    pppppuVar18 = (undefined4 *****)ppppuStack_25c;
    if ((0xfff < local_248 + 1) &&
       (pppppuVar18 = (undefined4 *****)ppppuStack_25c[-1],
       0x1f < (uint)((int)ppppuStack_25c + (-4 - (int)pppppuVar18)))) {
      local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
      FUN_1009cac3();
    }
    FUN_10053fdd(pppppuVar18);
  }
  if (local_224 == (LIST_ENTRY *)0x2) {
    puVar14 = FUN_10020e70(&pvStack_254,&DAT_100fccd8,&DAT_100fcc90);
    local_8._0_1_ = 0x2d;
    puVar14 = FUN_10020fb0((uint *)&local_2e0,puVar14,&DAT_100fcd20);
    local_8._0_1_ = 0x2e;
    FUN_10007a40(&ppppuStack_304,puVar14);
    uStack_2ec = CONCAT71(uStack_2ec._1_7_,0x2e);
    pppppuVar18 = &ppppuStack_304;
    if ((LIST_ENTRY *)0xf < pLStack_2f0) {
      pppppuVar18 = (undefined4 *****)ppppuStack_304;
    }
    uStack_2ec = CONCAT44(pppppuVar18,(undefined4)uStack_2ec);
    local_8._0_1_ = 0x2f;
    pcVar16 = (char *)FUN_10025600(local_294,(undefined1 *)&local_2c8,(uint *)&ppppuStack_304);
    pcVar17 = pcVar16 + 1;
    if (*pcVar16 == '\0') {
      pcVar17 = "";
    }
    local_8._0_1_ = 0x2e;
    uVar6 = (undefined1)local_8;
    local_8._0_1_ = 0x2e;
    *(char *)((int)&(p_Var4->ProcessLocksList).Blink + 1) = *pcVar17;
    if ((LIST_ENTRY *)0xf < pLStack_2f0) {
      pppppuVar18 = (undefined4 *****)ppppuStack_304;
      if (((undefined1 *)0xfff < (undefined1 *)((int)&pLStack_2f0->Flink + 1U)) &&
         (pppppuVar18 = (undefined4 *****)ppppuStack_304[-1],
         0x1f < (uint)((int)ppppuStack_304 + (-4 - (int)pppppuVar18)))) {
        local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pppppuVar18);
    }
    local_8._0_1_ = 0x2d;
    uVar6 = (undefined1)local_8;
    local_8._0_1_ = 0x2d;
    uStack_2f4 = 0;
    pLStack_2f0 = (LIST_ENTRY *)0xf;
    ppppuStack_304 = (undefined4 ****)((uint)ppppuStack_304 & 0xffffff00);
    if (0xf < local_2cc) {
      pvVar24 = local_2e0;
      if ((0xfff < local_2cc + 1) &&
         (pvVar24 = *(void **)((int)local_2e0 + -4),
         0x1f < (uint)((int)local_2e0 + (-4 - (int)pvVar24)))) {
        local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pvVar24);
    }
    local_8._0_1_ = 0x27;
    uVar6 = (undefined1)local_8;
    local_8._0_1_ = 0x27;
    local_2d0 = 0;
    local_2cc = 0xf;
    local_2e0 = (void *)((uint)local_2e0 & 0xffffff00);
    if (0xf < local_244._4_4_) {
      pvVar24 = pvStack_254;
      if ((0xfff < local_244._4_4_ + 1) &&
         (pvVar24 = *(void **)((int)pvStack_254 - 4),
         0x1f < (uint)((int)pvStack_254 + (-4 - (int)pvVar24)))) {
        local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pvVar24);
    }
    puVar14 = FUN_10020e70(&pvStack_254,&DAT_100fcd50,&DAT_100fcc90);
    local_8._0_1_ = 0x30;
    puVar14 = FUN_10020fb0((uint *)&local_2e0,puVar14,&DAT_100fcd20);
    local_8._0_1_ = 0x31;
    FUN_10007a40(&ppppuStack_304,puVar14);
    uStack_2ec = CONCAT71(uStack_2ec._1_7_,0x2e);
    pppppuVar18 = &ppppuStack_304;
    if ((LIST_ENTRY *)0xf < pLStack_2f0) {
      pppppuVar18 = (undefined4 *****)ppppuStack_304;
    }
    uStack_2ec = CONCAT44(pppppuVar18,(undefined4)uStack_2ec);
    local_8._0_1_ = 0x32;
    pcVar16 = (char *)FUN_10025600(local_294,(undefined1 *)&local_2c8,(uint *)&ppppuStack_304);
    pcVar17 = pcVar16 + 1;
    if (*pcVar16 == '\0') {
      pcVar17 = "";
    }
    local_8._0_1_ = 0x31;
    uVar6 = (undefined1)local_8;
    local_8._0_1_ = 0x31;
    *(char *)((int)&(p_Var4->ProcessLocksList).Blink + 2) = *pcVar17;
    if ((LIST_ENTRY *)0xf < pLStack_2f0) {
      pppppuVar18 = (undefined4 *****)ppppuStack_304;
      if (((undefined1 *)0xfff < (undefined1 *)((int)&pLStack_2f0->Flink + 1U)) &&
         (pppppuVar18 = (undefined4 *****)ppppuStack_304[-1],
         0x1f < (uint)((int)ppppuStack_304 + (-4 - (int)pppppuVar18)))) {
        local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pppppuVar18);
    }
    local_8._0_1_ = 0x30;
    uVar6 = (undefined1)local_8;
    local_8._0_1_ = 0x30;
    uStack_2f4 = 0;
    pLStack_2f0 = (LIST_ENTRY *)0xf;
    ppppuStack_304 = (undefined4 ****)((uint)ppppuStack_304 & 0xffffff00);
    if (0xf < local_2cc) {
      pvVar24 = local_2e0;
      if ((0xfff < local_2cc + 1) &&
         (pvVar24 = *(void **)((int)local_2e0 + -4),
         0x1f < (uint)((int)local_2e0 + (-4 - (int)pvVar24)))) {
        local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pvVar24);
    }
    local_8._0_1_ = 0x27;
    uVar6 = (undefined1)local_8;
    local_8._0_1_ = 0x27;
    local_2d0 = 0;
    local_2cc = 0xf;
    local_2e0 = (void *)((uint)local_2e0 & 0xffffff00);
    if (0xf < local_244._4_4_) {
      pvVar24 = pvStack_254;
      if ((0xfff < local_244._4_4_ + 1) &&
         (pvVar24 = *(void **)((int)pvStack_254 - 4),
         0x1f < (uint)((int)pvStack_254 + (-4 - (int)pvVar24)))) {
        local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pvVar24);
    }
    puVar14 = FUN_10020e70(&pvStack_254,&DAT_100fcd08,&DAT_100fcc90);
    local_8._0_1_ = 0x33;
    puVar14 = FUN_10020fb0((uint *)&local_2e0,puVar14,&DAT_100fcd20);
    local_8._0_1_ = 0x34;
    FUN_10007a40(&ppppuStack_304,puVar14);
    uStack_2ec = CONCAT71(uStack_2ec._1_7_,0x2e);
    pppppuVar18 = &ppppuStack_304;
    if ((LIST_ENTRY *)0xf < pLStack_2f0) {
      pppppuVar18 = (undefined4 *****)ppppuStack_304;
    }
    uStack_2ec = CONCAT44(pppppuVar18,(undefined4)uStack_2ec);
    local_8._0_1_ = 0x35;
    pcVar16 = (char *)FUN_10025600(local_294,(undefined1 *)&local_2c8,(uint *)&ppppuStack_304);
    pcVar17 = pcVar16 + 1;
    if (*pcVar16 == '\0') {
      pcVar17 = "";
    }
    local_8._0_1_ = 0x34;
    uVar6 = (undefined1)local_8;
    local_8._0_1_ = 0x34;
    *(char *)((int)&(p_Var4->ProcessLocksList).Blink + 3) = *pcVar17;
    if ((LIST_ENTRY *)0xf < pLStack_2f0) {
      pppppuVar18 = (undefined4 *****)ppppuStack_304;
      if (((undefined1 *)0xfff < (undefined1 *)((int)&pLStack_2f0->Flink + 1U)) &&
         (pppppuVar18 = (undefined4 *****)ppppuStack_304[-1],
         0x1f < (uint)((int)ppppuStack_304 + (-4 - (int)pppppuVar18)))) {
        local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pppppuVar18);
    }
    local_8._0_1_ = 0x33;
    uVar6 = (undefined1)local_8;
    local_8._0_1_ = 0x33;
    uStack_2f4 = 0;
    pLStack_2f0 = (LIST_ENTRY *)0xf;
    ppppuStack_304 = (undefined4 ****)((uint)ppppuStack_304 & 0xffffff00);
    if (0xf < local_2cc) {
      pvVar24 = local_2e0;
      if ((0xfff < local_2cc + 1) &&
         (pvVar24 = *(void **)((int)local_2e0 + -4),
         0x1f < (uint)((int)local_2e0 + (-4 - (int)pvVar24)))) {
        local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pvVar24);
    }
    local_8._0_1_ = 0x27;
    local_2d0 = 0;
    local_2cc = 0xf;
    local_2e0 = (void *)((uint)local_2e0 & 0xffffff00);
    if (0xf < local_244._4_4_) {
      pvVar24 = pvStack_254;
      if ((0xfff < local_244._4_4_ + 1) &&
         (pvVar24 = *(void **)((int)pvStack_254 - 4),
         0x1f < (uint)((int)pvStack_254 + (-4 - (int)pvVar24)))) {
                    /* WARNING: Subroutine does not return */
        FUN_1009cac3();
      }
      FUN_10053fdd(pvVar24);
    }
  }
  puVar14 = FUN_10020e70(&pvStack_254,&DAT_100fccd8,&DAT_100fcc90);
  local_8._0_1_ = 0x36;
  puVar14 = FUN_10020fb0((uint *)&local_2e0,puVar14,&DAT_100fcca8);
  local_8._0_1_ = 0x37;
  FUN_10007a40(&ppppuStack_304,puVar14);
  uStack_2ec = CONCAT71(uStack_2ec._1_7_,0x2e);
  pppppuVar18 = &ppppuStack_304;
  if ((LIST_ENTRY *)0xf < pLStack_2f0) {
    pppppuVar18 = (undefined4 *****)ppppuStack_304;
  }
  uStack_2ec = CONCAT44(pppppuVar18,(undefined4)uStack_2ec);
  local_8._0_1_ = 0x38;
  pcVar16 = (char *)FUN_10025510(local_294,(undefined1 *)&local_2c8,(uint *)&ppppuStack_304);
  pcVar17 = pcVar16 + 1;
  if (*pcVar16 == '\0') {
    pcVar17 = "";
  }
  local_8._0_1_ = 0x37;
  uVar6 = (undefined1)local_8;
  local_8._0_1_ = 0x37;
  *(char *)&p_Var4->EntryCount = *pcVar17;
  if ((LIST_ENTRY *)0xf < pLStack_2f0) {
    pppppuVar18 = (undefined4 *****)ppppuStack_304;
    if (((undefined1 *)0xfff < (undefined1 *)((int)&pLStack_2f0->Flink + 1U)) &&
       (pppppuVar18 = (undefined4 *****)ppppuStack_304[-1],
       0x1f < (uint)((int)ppppuStack_304 + (-4 - (int)pppppuVar18)))) {
      local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
      FUN_1009cac3();
    }
    FUN_10053fdd(pppppuVar18);
  }
  local_8._0_1_ = 0x36;
  uVar6 = (undefined1)local_8;
  local_8._0_1_ = 0x36;
  uStack_2f4 = 0;
  pLStack_2f0 = (LIST_ENTRY *)0xf;
  ppppuStack_304 = (undefined4 ****)((uint)ppppuStack_304 & 0xffffff00);
  if (0xf < local_2cc) {
    pvVar24 = local_2e0;
    if ((0xfff < local_2cc + 1) &&
       (pvVar24 = *(void **)((int)local_2e0 + -4),
       0x1f < (uint)((int)local_2e0 + (-4 - (int)pvVar24)))) {
      local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
      FUN_1009cac3();
    }
    FUN_10053fdd(pvVar24);
  }
  local_8._0_1_ = 0x27;
  uVar6 = (undefined1)local_8;
  local_8._0_1_ = 0x27;
  local_2d0 = 0;
  local_2cc = 0xf;
  local_2e0 = (void *)((uint)local_2e0 & 0xffffff00);
  if (0xf < local_244._4_4_) {
    pvVar24 = pvStack_254;
    if ((0xfff < local_244._4_4_ + 1) &&
       (pvVar24 = *(void **)((int)pvStack_254 - 4),
       0x1f < (uint)((int)pvStack_254 + (-4 - (int)pvVar24)))) {
      local_8._0_1_ = uVar6;
                    /* WARNING: Subroutine does not return */
      FUN_1009cac3();
    }
    FUN_10053fdd(pvVar24);
  }
  puVar14 = FUN_10020e70(&local_2e0,&DAT_100fcd50,&DAT_100fcc90);
  local_8._0_1_ = 0x39;
  puVar14 = FUN_10020fb0((uint *)&pvStack_254,puVar14,&DAT_100fcca8);
  local_8._0_1_ = 0x3a;
  FUN_10007a40(&ppppuStack_304,puVar14);
  uStack_2ec = CONCAT71(uStack_2ec._1_7_,0x2e);
  pppppuVar18 = &ppppuStack_304;
  if ((LIST_ENTRY *)0xf < pLStack_2f0) {
    pppppuVar18 = (undefined4 *****)ppppuStack_304;
  }
  uStack_2ec = CONCAT44(pppppuVar18,(undefined4)uStack_2ec);
  local_8._0_1_ = 0x3b;
  pcVar16 = (char *)FUN_10025510(local_294,(undefined1 *)&local_2c8,(uint *)&ppppuStack_304);
  pcVar17 = pcVar16 + 1;
  if (*pcVar16 == '\0') {
    pcVar17 = "";
  }
  *(char *)((int)&p_Var4->EntryCount + 1) = *pcVar17;
  FUN_10002f70((int *)&ppppuStack_304);
  FUN_10002f70((int *)&pvStack_254);
  local_8._0_1_ = 0x27;
  FUN_10002f70((int *)&local_2e0);
  puVar14 = FUN_10020e70(&local_2e0,&DAT_100fcd08,&DAT_100fcc90);
  local_8._0_1_ = 0x3c;
  puVar14 = FUN_10020fb0((uint *)&pvStack_254,puVar14,&DAT_100fcca8);
  local_8._0_1_ = 0x3d;
  FUN_10020a50(&ppppuStack_304,puVar14);
  local_8._0_1_ = 0x3e;
  cVar7 = FUN_100212e0(local_294,(uint *)&ppppuStack_304,"");
  *(char *)((int)&p_Var4->EntryCount + 2) = cVar7;
  FUN_10002f70((int *)&ppppuStack_304);
  FUN_10002f70((int *)&pvStack_254);
  local_8._0_1_ = 0x27;
  FUN_10002f70((int *)&local_2e0);
  FUN_10020a50(&ppppuStack_25c,&DAT_100fccf0);
  local_8 = CONCAT31(local_8._1_3_,0x3f);
  DVar19 = FUN_10021310(local_294,(uint *)&ppppuStack_25c);
  p_Var4->ContentionCount = DVar19;
  FUN_10002f70((int *)&ppppuStack_25c);
  local_8 = 0x23;
  FUN_10011a99();
  return;
}


```

## ConfigInit_100013f0 @ 0x100013f0

**Strings referenced (max 60):**
- 0x100013f2 → 0x100e0714  `options.json`

```c

void ConfigInit_100013f0(void)

{
  FUN_100030d0(&DAT_100fcd68,(uint *)"options.json",0xc);
  _atexit(FUN_100cbb80);
  return;
}


```

## ConfigInit_10001770 @ 0x10001770

**Strings referenced (max 60):**
- 0x10001772 → 0x100e0714  `options.json`

```c

void ConfigInit_10001770(void)

{
  FUN_100030d0(&DAT_100fce58,(uint *)"options.json",0xc);
  _atexit(FUN_100cbfd0);
  return;
}


```

## ConfigInit_10001ac0 @ 0x10001ac0

**Strings referenced (max 60):**
- 0x10001ac2 → 0x100e0714  `options.json`

```c

void ConfigInit_10001ac0(void)

{
  FUN_100030d0(&DAT_100fcf78,(uint *)"options.json",0xc);
  _atexit(FUN_100cc470);
  return;
}


```

## FUN_10010280 @ 0x10010280

**Strings referenced (max 60):**
- 0x1001034d → 0x100e0b30  `!!cs_close_device();`
- 0x10010364 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x10010369 → 0x100e1330  `m_pStreamCompound != 0`

```c

/* WARNING: Removing unreachable block (ram,0x1001047c) */

void __fastcall FUN_10010280(void *param_1)

{
  wchar_t *pwVar1;
  void *this;
  undefined4 *puVar2;
  int iVar3;
  byte ******ppppppbVar4;
  undefined4 ******ppppppuVar5;
  uint unaff_EDI;
  undefined4 *in_stack_fffffecc;
  undefined4 uVar6;
  void **ppvVar7;
  int *piVar8;
  char *pcVar9;
  wchar_t *pwVar10;
  undefined *local_114 [4];
  int local_104 [41];
  undefined4 *****local_60 [4];
  uint local_50;
  uint local_4c;
  int local_48;
  undefined4 *local_44;
  undefined4 local_40;
  undefined4 local_3c;
  byte *****local_38 [4];
  int local_28;
  uint local_24;
  void *local_20;
  undefined8 local_1c;
  undefined4 *****local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_100c2383;
  local_10 = ExceptionList;
  pwVar1 = (wchar_t *)(DAT_100fc0f4 ^ (uint)&stack0xfffffffc);
  ExceptionList = &local_10;
  local_14 = (undefined4 *****)pwVar1;
  if (*(char *)((int)param_1 + 0x25c) != '\0') {
    if (*(byte *)((int)param_1 + 0xc) < 5) {
      local_20 = (void *)0x0;
      local_1c = CONCAT44(&local_3c,(uint)local_1c);
      puVar2 = (undefined4 *)((int)&local_1c + 4);
      ppvVar7 = &local_20;
      local_3c = 1;
      this = (void *)FUN_1005f320();
      FUN_10020d90(this,ppvVar7,puVar2);
      local_8 = 0;
      while (local_20 != (void *)0x0) {
        FUN_10007bd0((int *)local_114);
        local_8._0_1_ = 1;
        local_48 = FUN_1005f320();
        puVar2 = FUN_100573c0(&local_20);
        local_44 = puVar2;
        local_40 = ___uncaught_exceptions();
        piVar8 = local_104;
        local_8 = CONCAT31(local_8._1_3_,2);
        pcVar9 = "!!cs_close_device();";
        uVar6 = 0x10010358;
        FUN_1000b420(piVar8,"!!cs_close_device();");
        if (puVar2 == (undefined4 *)0x0) {
          unaff_EDI = 0x216;
          pwVar1 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
          pwVar10 = L"m_pStreamCompound != 0";
          piVar8 = (int *)0x10010373;
          FID_conflict___assert
                    (L"m_pStreamCompound != 0",
                     L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216
                    );
          pcVar9 = (char *)pwVar10;
        }
        FUN_10007b10(local_114,&stack0xfffffecc);
        FUN_10031fd0(local_38,in_stack_fffffecc,uVar6,piVar8,pcVar9,(uint)pwVar1,unaff_EDI);
        local_8._0_1_ = 3;
        ppppppbVar4 = local_38;
        if (0xf < local_24) {
          ppppppbVar4 = (byte ******)local_38[0];
        }
        FUN_10031d60(local_60,(byte *)ppppppbVar4,local_28);
        local_8._0_1_ = 2;
        if (0xf < local_24) {
          ppppppbVar4 = (byte ******)local_38[0];
          if ((0xfff < local_24 + 1) &&
             (ppppppbVar4 = (byte ******)local_38[0][-1],
             (byte *)0x1f < (byte *)((int)local_38[0] + (-4 - (int)ppppppbVar4))))
          goto LAB_10010544;
          FUN_10053fdd(ppppppbVar4);
        }
        local_28 = 0;
        local_24 = 0xf;
        local_38[0] = (byte *****)((uint)local_38[0] & 0xffffff00);
        local_8._0_1_ = 4;
        pwVar1 = (wchar_t *)local_60;
        if (0xf < local_4c) {
          pwVar1 = (wchar_t *)local_60[0];
        }
        unaff_EDI = local_50;
        FUN_1000c2f0(puVar2 + 0x18,pwVar1,local_50);
        local_8._0_1_ = 2;
        if (0xf < local_4c) {
          local_114[0] = (undefined *)(local_4c + 1);
          ppppppuVar5 = (undefined4 ******)local_60[0];
          if ((undefined *)0xfff < local_114[0]) {
            ppppppuVar5 = (undefined4 ******)local_60[0][-1];
            local_114[0] = (undefined *)(local_4c + 0x24);
            if (0x1f < (uint)((int)local_60[0] + (-4 - (int)ppppppuVar5))) {
LAB_10010544:
              local_8._0_1_ = 2;
                    /* WARNING: Subroutine does not return */
              local_114[0] = &UNK_10010549;
              FUN_1009cac3();
            }
          }
          FUN_10053fdd(ppppppuVar5);
        }
        local_8._0_1_ = 1;
        local_114[0] = (undefined *)0x10010457;
        FUN_1001d730(&local_48);
        local_8 = (uint)local_8._1_3_ << 8;
        local_114[0] = (undefined *)0x10010466;
        FUN_10004940((int *)local_114);
      }
      local_20 = (void *)0x0;
    }
    local_8 = 0xffffffff;
    if (*(char *)((int)param_1 + 0x25d) == '\0') {
      local_1c = 0;
      FUN_1001d270(param_1,0x20,(uint *)0x0,0,(uint *)&local_1c,3000);
    }
    FUN_1001d950((int *)((int)param_1 + 0x48));
    local_1c = ZEXT48((_Mtx_internal_imp_t *)((int)param_1 + 0xb0));
    iVar3 = __Mtx_lock((_Mtx_internal_imp_t *)((int)param_1 + 0xb0));
    if (iVar3 != 0) {
      std::_Throw_C_error(iVar3);
    }
    local_1c._0_5_ = CONCAT14(1,(uint)local_1c);
    local_8 = 5;
    FUN_1001f160((int)param_1 + 0x160);
    FUN_1001de30((int *)&local_1c);
    *(undefined1 *)((int)param_1 + 0x25c) = 0;
    local_8 = 6;
    if (local_1c._4_1_ != '\0') {
      iVar3 = __Mtx_unlock((uint)local_1c);
      if (iVar3 != 0) {
        std::_Throw_C_error(iVar3);
      }
    }
  }
  ExceptionList = local_10;
  __security_check_cookie((uint)local_14 ^ (uint)&stack0xfffffffc);
  return;
}


```

## FUN_100101b0 @ 0x100101b0

**Strings referenced (max 60):**
- _(none)_

```c

void __fastcall FUN_100101b0(int *param_1)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  int *piVar4;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB_100c2330;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  iVar1 = *param_1;
  local_8 = 0;
  iVar3 = iVar1;
  piVar4 = *(int **)(iVar1 + 4);
  if (*(char *)((int)*(int **)(iVar1 + 4) + 0xd) == '\0') {
    do {
      FUN_10020540((int *)piVar4[2]);
      piVar2 = (int *)*piVar4;
      FUN_10053fdd(piVar4);
      piVar4 = piVar2;
    } while (*(char *)((int)piVar2 + 0xd) == '\0');
    iVar3 = *param_1;
  }
  *(int *)(iVar3 + 4) = iVar1;
  *(int *)*param_1 = iVar1;
  *(int *)(*param_1 + 8) = iVar1;
  param_1[1] = 0;
  FUN_10053fdd((void *)*param_1);
  ExceptionList = local_10;
  return;
}


```

## FUN_10010250 @ 0x10010250

**Strings referenced (max 60):**
- _(none)_

```c

void __fastcall FUN_10010250(undefined4 *param_1)

{
  undefined4 *local_8;
  
  local_8 = param_1;
  FUN_1001f400(param_1,&local_8,*(int **)*param_1,(int *)*param_1);
  FUN_10053fdd((void *)*param_1);
  return;
}


```


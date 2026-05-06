# Ghidra wire envelope — j2534_interface.dll

Round 4: chase the bytes-on-wire format via send-and-wait helper + IOCP drain thread.

## Callers of device_write_async (FUN_1003dca0 / WriteFile)

- 0x1003bb94  ←  FUN_1003bb10 @ 0x1003bb10

## Callers of GetQueuedCompletionStatus (IOCP pump)

- 0x10038bfb  ←  FUN_10038aa0 @ 0x10038aa0
- 0x100388cb  ←  FUN_10038770 @ 0x10038770

## Callers of CreateThread

- 0x100a66e3  ←  __beginthreadex @ 0x100a669a
- 0x1007f09e  ←  __CreateThread @ 0x1007f089

### send_and_wait (FUN_1001d270 — used by both transports) — 0x1001d270

**Strings referenced (max 30):**
- 0x1001d3eb → 0x100e1298  ` execRequest result = `
- 0x1001d421 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001d426 → 0x100e1330  `m_pStreamCompound != 0`

```c

void __thiscall
FUN_1001d270(void *this,uint param_1,uint *param_2,ushort param_3,uint *param_4,uint param_5)

{
  uint *puVar1;
  undefined1 uVar2;
  int iVar3;
  uint uVar4;
  uint *puVar5;
  void *this_00;
  undefined4 *puVar6;
  byte ****ppppbVar7;
  undefined4 ****ppppuVar8;
  undefined4 unaff_EBX;
  int *piVar9;
  uint **ppuVar10;
  undefined *puVar11;
  wchar_t *in_stack_fffffed0;
  wchar_t *pwVar12;
  wchar_t *in_stack_fffffed4;
  uint in_stack_fffffed8;
  int local_80;
  undefined4 *local_7c;
  undefined4 local_78;
  undefined4 ***local_74 [4];
  uint local_64;
  uint local_60;
  _Mtx_internal_imp_t *local_5c;
  uint local_58;
  uint *local_54;
  byte ***local_50 [4];
  int local_40;
  uint local_3c;
  undefined4 ***local_38 [4];
  uint local_28;
  uint local_24;
  uint local_20;
  int local_1c;
  uint local_18;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8._0_1_ = 0xff;
  local_8._1_3_ = 0xffffff;
  puStack_c = &LAB_100c3693;
  local_10 = ExceptionList;
  local_18 = DAT_100fc0f4 ^ (uint)&stack0xfffffffc;
  ExceptionList = &local_10;
  local_5c = (_Mtx_internal_imp_t *)((int)this + 0x50);
  iVar3 = __Mtx_lock(local_5c);
  if (iVar3 != 0) {
    std::_Throw_C_error(iVar3);
  }
  uVar4 = FUN_1001c810(this,param_1,param_2,param_3,param_4,param_5);
  local_58 = uVar4;
  if (4 < *(byte *)((int)this + 0xc)) goto LAB_1001d588;
  puVar1 = *(uint **)((int)this + 4);
  puVar5 = *(uint **)this;
  local_20 = uVar4;
  if (puVar5 == puVar1) {
LAB_1001d2ff:
    if (*(uint **)((int)this + 8) == puVar1) {
      FUN_10021980(this,puVar1,&local_20);
    }
    else {
      *puVar1 = uVar4;
      *(int *)((int)this + 4) = *(int *)((int)this + 4) + 4;
    }
  }
  else {
    do {
      if (*puVar5 == uVar4) break;
      puVar5 = puVar5 + 1;
    } while (puVar5 != puVar1);
    if (puVar5 == puVar1) goto LAB_1001d2ff;
  }
  local_28 = 0;
  local_24 = 0xf;
  local_38[0] = (undefined4 ***)((uint)local_38[0] & 0xffffff00);
  FUN_100030d0(local_38,(uint *)&DAT_100e0149,0);
  local_8 = 0;
  if (uVar4 != 0) {
    FUN_100030d0(local_38,(uint *)&DAT_100e1294,3);
  }
  local_54 = &local_20;
  local_1c = 0;
  ppuVar10 = &local_54;
  piVar9 = &local_1c;
  local_20 = 1;
  this_00 = (void *)FUN_1005f320();
  FUN_10020d90(this_00,piVar9,ppuVar10);
  local_8._0_1_ = 1;
  while (local_1c != 0) {
    FUN_10007bd0((int *)&stack0xfffffed0);
    local_8._0_1_ = 2;
    local_80 = FUN_1005f320();
    puVar6 = FUN_100573c0(&local_1c);
    local_7c = puVar6;
    local_78 = ___uncaught_exceptions();
    local_8 = CONCAT31(local_8._1_3_,3);
    ppppuVar8 = local_38;
    if (0xf < local_24) {
      ppppuVar8 = (undefined4 ****)local_38[0];
    }
    FUN_1000c2f0((int *)&stack0xfffffee0,ppppuVar8,local_28);
    FUN_1000b420((int *)&stack0xfffffee0," execRequest result = ");
    FUN_10036160((int *)&stack0xfffffee0,&local_58);
    piVar9 = (int *)&stack0xfffffee0;
    puVar11 = &DAT_100e021c;
    FUN_1000b420(piVar9,"\n\n");
    if (puVar6 == (undefined4 *)0x0) {
      in_stack_fffffed8 = 0x216;
      in_stack_fffffed4 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
      in_stack_fffffed0 = L"m_pStreamCompound != 0";
      unaff_EBX = 0x1001d430;
      FID_conflict___assert
                (L"m_pStreamCompound != 0",
                 L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216);
    }
    pwVar12 = (wchar_t *)(puVar6 + 0x18);
    FUN_10007b10(&stack0xfffffed0,&stack0xfffffec4);
    FUN_10031fd0(local_50,piVar9,puVar11,unaff_EBX,in_stack_fffffed0,(uint)in_stack_fffffed4,
                 in_stack_fffffed8);
    local_8._0_1_ = 4;
    ppppbVar7 = local_50;
    if (0xf < local_3c) {
      ppppbVar7 = (byte ****)local_50[0];
    }
    FUN_10031d60(local_74,(byte *)ppppbVar7,local_40);
    local_8._0_1_ = 3;
    uVar2 = (undefined1)local_8;
    local_8._0_1_ = 3;
    if (0xf < local_3c) {
      ppppbVar7 = (byte ****)local_50[0];
      if ((0xfff < local_3c + 1) &&
         (ppppbVar7 = (byte ****)local_50[0][-1],
         (byte *)0x1f < (byte *)((int)local_50[0] + (-4 - (int)ppppbVar7)))) goto LAB_1001d5c0;
      FUN_10053fdd(ppppbVar7);
    }
    local_40 = 0;
    local_3c = 0xf;
    local_50[0] = (byte ***)((uint)local_50[0] & 0xffffff00);
    local_8._0_1_ = 5;
    in_stack_fffffed4 = (wchar_t *)local_74;
    if (0xf < local_60) {
      in_stack_fffffed4 = (wchar_t *)local_74[0];
    }
    unaff_EBX = 0x1001d4cd;
    in_stack_fffffed8 = local_64;
    FUN_1000c2f0((int *)pwVar12,in_stack_fffffed4,local_64);
    local_8._0_1_ = 3;
    if (0xf < local_60) {
      ppppuVar8 = (undefined4 ****)local_74[0];
      if ((0xfff < local_60 + 1) &&
         (ppppuVar8 = (undefined4 ****)local_74[0][-1], uVar2 = (undefined1)local_8,
         0x1f < (uint)((int)local_74[0] + (-4 - (int)ppppuVar8)))) goto LAB_1001d5c0;
      FUN_10053fdd(ppppuVar8);
    }
    local_64 = 0;
    local_60 = 0xf;
    local_74[0] = (undefined4 ***)((uint)local_74[0] & 0xffffff00);
    local_8._0_1_ = 2;
    FUN_1001d730(&local_80);
    local_8._0_1_ = 1;
    FUN_10004940((int *)&stack0xfffffed0);
    in_stack_fffffed0 = pwVar12;
  }
  local_8._0_1_ = 0xff;
  local_8._1_3_ = 0xffffff;
  if (0xf < local_24) {
    ppppuVar8 = (undefined4 ****)local_38[0];
    if ((0xfff < local_24 + 1) &&
       (ppppuVar8 = (undefined4 ****)local_38[0][-1], uVar2 = (undefined1)local_8,
       0x1f < (uint)((int)local_38[0] + (-4 - (int)ppppuVar8)))) {
LAB_1001d5c0:
      local_8._0_1_ = uVar2;
                    /* WARNING: Subroutine does not return */
      FUN_1009cac3();
    }
    FUN_10053fdd(ppppuVar8);
  }
  local_28 = 0;
  local_24 = 0xf;
  local_38[0] = (undefined4 ***)((uint)local_38[0] & 0xffffff00);
LAB_1001d588:
  iVar3 = __Mtx_unlock((int)local_5c);
  if (iVar3 != 0) {
    std::_Throw_C_error(iVar3);
  }
  ExceptionList = local_10;
  __security_check_cookie(local_18 ^ (uint)&stack0xfffffffc);
  return;
}


```

## IOCP drain / device_write_async caller(s) — auto-detected

### FUN_1003bb10 — 0x1003bb10

**Strings referenced (max 30):**
- 0x1003bc46 → 0x100e5110  `write`

```c

void __fastcall FUN_1003bb10(int *param_1,int *param_2)

{
  int iVar1;
  uint uVar2;
  char cVar3;
  int *piVar4;
  char cVar5;
  uint uVar6;
  undefined4 in_stack_ffffffac;
  undefined4 in_stack_ffffffb0;
  DWORD local_2c;
  undefined **local_28;
  int local_24;
  int local_20;
  char local_1c [4];
  int local_18;
  uint local_14;
  int *local_10;
  int local_c;
  uint local_8;
  
  local_8 = DAT_100fc0f4 ^ (uint)&stack0xfffffffc;
  FUN_10055c00();
  local_28 = FUN_10055c00();
  cVar5 = '\0';
  local_2c = 0;
  local_1c[1] = '\0';
  local_1c[2] = '\0';
  local_c = 0x10000;
  local_1c[3] = 0;
  local_24 = *param_2;
  local_20 = param_2[1];
  local_18 = *param_2;
  local_14 = param_2[1];
  local_10 = (int *)local_1c;
  local_1c[0] = '\0';
  do {
    cVar3 = '\x01';
    if (local_c != 0) {
      cVar3 = cVar5;
    }
    if (cVar3 != '\0') {
      if (local_2c != 0) {
                    /* WARNING: Subroutine does not return */
        FUN_1000ddf0(&local_2c,"write");
      }
      __security_check_cookie(local_8 ^ (uint)&stack0xfffffffc);
      return;
    }
    uVar2 = FUN_1003dca0(param_1,in_stack_ffffffac,in_stack_ffffffb0,(int)&local_24,&local_2c);
    cVar5 = local_1c[0];
    iVar1 = local_18;
    uVar6 = local_14;
    piVar4 = local_10;
    while (uVar2 != 0) {
      if (cVar5 != '\0') goto LAB_1003bc15;
      if (uVar2 < uVar6) {
        local_18 = iVar1 + uVar2;
        uVar6 = uVar6 - uVar2;
        local_14 = uVar6;
        goto LAB_1003bbe1;
      }
      uVar2 = uVar2 - uVar6;
      if (piVar4 == (int *)local_1c) {
        cVar5 = '\x01';
        local_1c[0] = '\x01';
      }
      else {
        iVar1 = *piVar4;
        uVar6 = piVar4[1];
        piVar4 = piVar4 + 2;
        local_18 = iVar1;
        local_14 = uVar6;
        local_10 = piVar4;
      }
    }
    while (cVar5 == '\0') {
LAB_1003bbe1:
      if (uVar6 != 0) break;
      if (piVar4 == (int *)local_1c) {
        cVar5 = '\x01';
        local_1c[0] = '\x01';
        break;
      }
      local_18 = *piVar4;
      uVar6 = piVar4[1];
      piVar4 = piVar4 + 2;
      local_14 = uVar6;
      local_10 = piVar4;
    }
LAB_1003bc15:
    local_c = 0x10000;
    if (local_2c != 0) {
      local_c = 0;
    }
  } while( true );
}


```

### FUN_10038aa0 — 0x10038aa0

**Strings referenced (max 30):**
- _(none)_

```c

void __thiscall FUN_10038aa0(void *this,undefined4 param_1,DWORD *param_2)

{
  int *piVar1;
  LPOVERLAPPED p_Var2;
  BOOL BVar3;
  DWORD DVar4;
  undefined **ppuVar5;
  int iVar6;
  int *piVar7;
  LPOVERLAPPED local_38;
  LARGE_INTEGER local_34;
  DWORD local_2c;
  undefined **local_28;
  undefined8 local_24;
  ulong local_1c;
  DWORD local_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_100c5338;
  local_10 = ExceptionList;
  local_14 = DAT_100fc0f4 ^ (uint)&stack0xfffffffc;
  ExceptionList = &local_10;
LAB_10038ae0:
  while( true ) {
    LOCK();
    iVar6 = *(int *)((int)this + 0x34);
    if (iVar6 == 1) {
      *(int *)((int)this + 0x34) = 0;
      iVar6 = 1;
    }
    UNLOCK();
    if (iVar6 == 1) {
      EnterCriticalSection((LPCRITICAL_SECTION)((int)this + 0x38));
      local_24 = 0;
      local_8 = 1;
      if (*(int *)((int)this + 0x54) != 0) {
        local_24 = CONCAT44(*(undefined4 *)((int)this + 0x58),*(int *)((int)this + 0x54));
        *(undefined4 *)((int)this + 0x54) = 0;
        *(undefined4 *)((int)this + 0x58) = 0;
      }
      for (piVar7 = *(int **)((int)this + 0x50); piVar7 != (int *)0x0; piVar7 = (int *)piVar7[1]) {
        (**(code **)(*piVar7 + 0x10))(&local_24);
      }
      FUN_1000dfb0(this,(ULONG_PTR *)&local_24);
      if (*(int *)((int)this + 0x2c) != 0) {
        piVar7 = *(int **)((int)this + 0x50);
        iVar6 = 300000000;
        if (piVar7 != (int *)0x0) {
          do {
            iVar6 = (**(code **)(*piVar7 + 0xc))(iVar6);
            piVar7 = (int *)piVar7[1];
          } while (piVar7 != (int *)0x0);
          if (iVar6 < 300000000) {
            local_34 = (LARGE_INTEGER)((longlong)-iVar6 * 10);
            SetWaitableTimer(*(HANDLE *)((int)this + 0x30),&local_34,300000,(PTIMERAPCROUTINE)0x0,
                             (LPVOID)0x0,0);
          }
        }
      }
      FUN_1001dc90((int *)&local_24);
      local_8 = 0xffffffff;
      LeaveCriticalSection((LPCRITICAL_SECTION)((int)this + 0x38));
    }
    local_18 = 0;
    local_1c = 0;
    local_38 = (LPOVERLAPPED)0x0;
    SetLastError(0);
    BVar3 = GetQueuedCompletionStatus
                      (*(HANDLE *)((int)this + 0x14),&local_18,&local_1c,&local_38,
                       *(DWORD *)((int)this + 0x28));
    DVar4 = GetLastError();
    p_Var2 = local_38;
    if (local_38 == (LPOVERLAPPED)0x0) break;
    local_28 = FUN_10055c00();
    if (local_1c == 2) {
      local_28 = (undefined **)p_Var2->Internal;
      local_18 = (p_Var2->u).s.OffsetHigh;
      local_2c = (p_Var2->u).s.Offset;
    }
    else {
      p_Var2->Internal = (ULONG_PTR)local_28;
      (p_Var2->u).s.Offset = DVar4;
      (p_Var2->u).s.OffsetHigh = local_18;
      local_2c = DVar4;
    }
    LOCK();
    DVar4 = p_Var2[1].u.s.Offset;
    if (DVar4 == 0) {
      p_Var2[1].u.s.Offset = 1;
      DVar4 = 0;
    }
    UNLOCK();
    if (DVar4 == 1) {
      local_8 = 2;
      (*(code *)p_Var2[1].InternalHigh)(this,p_Var2,&local_2c,local_18);
      ppuVar5 = FUN_10055c00();
      *param_2 = 0;
      param_2[1] = (DWORD)ppuVar5;
      local_8 = 3;
      LOCK();
      iVar6 = *(int *)((int)this + 0x18) + -1;
      *(int *)((int)this + 0x18) = iVar6;
      UNLOCK();
      if (iVar6 == 0) {
        FUN_100389b0((int)this);
      }
LAB_10038d33:
      ExceptionList = local_10;
      __security_check_cookie(local_14 ^ (uint)&stack0xfffffffc);
      return;
    }
  }
  if (BVar3 == 0) {
    if (DVar4 == 0x102) goto LAB_10038ae0;
    ppuVar5 = FUN_10055c00();
    *param_2 = DVar4;
  }
  else {
    if (local_1c == 1) goto LAB_10038ae0;
    piVar7 = (int *)((int)this + 0x20);
    LOCK();
    *piVar7 = 0;
    UNLOCK();
    piVar1 = (int *)((int)this + 0x1c);
    LOCK();
    iVar6 = *piVar1;
    *piVar1 = *piVar1;
    UNLOCK();
    if (iVar6 == 0) goto LAB_10038ae0;
    LOCK();
    iVar6 = *piVar7;
    *piVar7 = 1;
    UNLOCK();
    if (iVar6 == 0) {
      BVar3 = PostQueuedCompletionStatus(*(HANDLE *)((int)this + 0x14),0,0,(LPOVERLAPPED)0x0);
      if (BVar3 == 0) {
        DVar4 = GetLastError();
        ppuVar5 = FUN_10055c00();
        *param_2 = DVar4;
        goto LAB_10038d2e;
      }
    }
    ppuVar5 = FUN_10055c00();
    *param_2 = 0;
  }
LAB_10038d2e:
  param_2[1] = (DWORD)ppuVar5;
  goto LAB_10038d33;
}


```

### FUN_10038770 — 0x10038770

**Strings referenced (max 30):**
- _(none)_

```c

void __fastcall FUN_10038770(int param_1)

{
  int *piVar1;
  int iVar2;
  LPOVERLAPPED p_Var3;
  uint uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  int *piVar8;
  undefined4 local_38;
  undefined **local_34;
  LPOVERLAPPED local_30;
  DWORD local_2c;
  ulong local_28;
  LARGE_INTEGER local_24;
  HANDLE local_1c;
  undefined **local_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_100c52f8;
  local_10 = ExceptionList;
  uVar4 = DAT_100fc0f4 ^ (uint)&stack0xfffffffc;
  ExceptionList = &local_10;
  LOCK();
  *(undefined4 *)(param_1 + 0x24) = 1;
  UNLOCK();
  local_14 = uVar4;
  if (*(int *)(param_1 + 0x2c) != 0) {
    local_24.QuadPart = 4.94065645841247e-324;
    SetWaitableTimer(*(HANDLE *)(param_1 + 0x30),&local_24,1,(PTIMERAPCROUTINE)0x0,(LPVOID)0x0,0);
  }
  piVar1 = (int *)(param_1 + 0x18);
  LOCK();
  iVar2 = *piVar1;
  *piVar1 = *piVar1;
  UNLOCK();
  while (0 < iVar2) {
    local_24.s.LowPart = 0;
    local_24.QuadPart = 0.0;
    local_8 = 0;
    piVar8 = *(int **)(param_1 + 0x50);
    uVar7 = 0;
    if (piVar8 != (int *)0x0) {
      do {
        (**(code **)(*piVar8 + 0x14))(&local_24,uVar4);
        piVar8 = (int *)piVar8[1];
      } while (piVar8 != (int *)0x0);
      uVar7 = local_24.s.HighPart;
    }
    uVar5 = *(uint *)(param_1 + 0x54);
    uVar6 = local_24.s.LowPart;
    if (uVar5 != 0) {
      if (uVar7 == 0) {
        local_24.s.HighPart = 0;
        local_24.s.LowPart = uVar5;
      }
      else {
        *(undefined4 *)(uVar7 + 0x14) = uVar5;
        uVar5 = local_24.s.LowPart;
      }
      uVar7 = *(int *)(param_1 + 0x58);
      local_24.s.HighPart = uVar7;
      *(undefined4 *)(param_1 + 0x54) = 0;
      *(undefined4 *)(param_1 + 0x58) = 0;
      uVar6 = uVar5;
    }
    if (uVar6 == 0) {
      local_2c = 0;
      local_28 = 0;
      local_30 = (LPOVERLAPPED)0x0;
      GetQueuedCompletionStatus
                (*(HANDLE *)(param_1 + 0x14),&local_2c,&local_28,&local_30,
                 *(DWORD *)(param_1 + 0x28));
      p_Var3 = local_30;
      if (local_30 != (LPOVERLAPPED)0x0) {
        LOCK();
        *piVar1 = *piVar1 + -1;
        UNLOCK();
        local_1c = (HANDLE)0x0;
        local_18 = FUN_10055c00();
        (*(code *)p_Var3[1].InternalHigh)(0,p_Var3,&local_1c,0);
      }
    }
    else {
      while( true ) {
        if (uVar6 != 0) {
          local_30 = (LPOVERLAPPED)0x0;
          if (*(int *)(uVar6 + 0x14) == 0) {
            uVar7 = 0;
          }
          local_24.s.HighPart = uVar7;
          local_24.s.LowPart = *(int *)(uVar6 + 0x14);
          *(undefined4 *)(uVar6 + 0x14) = 0;
        }
        LOCK();
        *piVar1 = *piVar1 + -1;
        UNLOCK();
        local_38 = 0;
        local_34 = FUN_10055c00();
        (**(code **)(uVar6 + 0x18))(0,uVar6,&local_38,0);
        if (local_24.s.LowPart == 0) break;
        uVar7 = local_24.s.HighPart;
        uVar6 = local_24.s.LowPart;
      }
    }
    local_8 = 0xffffffff;
    FUN_1001dc90((int *)&local_24);
    LOCK();
    iVar2 = *piVar1;
    *piVar1 = *piVar1;
    UNLOCK();
  }
  iVar2 = *(int *)(param_1 + 0x2c);
  if (iVar2 != 0) {
    local_1c = *(HANDLE *)(iVar2 + 8);
    local_18 = *(undefined ***)(iVar2 + 4);
    WaitForMultipleObjects(2,&local_1c,0,0xffffffff);
    CloseHandle(*(HANDLE *)(iVar2 + 8));
    LOCK();
    UNLOCK();
    if (DAT_10104c60 == 0) {
      QueueUserAPC(FUN_10008540,*(HANDLE *)(iVar2 + 4),0);
      WaitForSingleObject(*(HANDLE *)(iVar2 + 4),0xffffffff);
    }
    else {
      TerminateThread(*(HANDLE *)(iVar2 + 4),0);
    }
  }
  ExceptionList = local_10;
  __security_check_cookie(local_14 ^ (uint)&stack0xfffffffc);
  return;
}


```


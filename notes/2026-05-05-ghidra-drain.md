# Ghidra drain — caller of FUN_1003bb10 (the bytes-to-WriteFile bridge)

## Direct callers of FUN_1003bb10

- 0x10039c9c  ←  FUN_10039c80 @ 0x10039c80

## Callers of those callers (one level up)

### Callers of FUN_10039c80
- 0x1001ca8e  ←  FUN_1001c810 @ 0x1001c810

## Decompiles — direct callers

### FUN_10039c80 — 0x10039c80

**Strings referenced (max 25):**
- _(none)_

```c

void __thiscall FUN_10039c80(void *this,int param_1,undefined4 param_2)

{
  int local_10;
  undefined4 local_c;
  
  local_c = param_2;
  local_10 = param_1;
  FUN_1003bb10((int *)((int)this + 0xc),&local_10);
  return;
}


```

## Decompiles — second-level (max 4)

### FUN_1001c810 — 0x1001c810

**Strings referenced (max 25):**
- 0x1001c933 → 0x100e1270  `(W) >> `
- 0x1001c95a → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001c95f → 0x100e1330  `m_pStreamCompound != 0`
- 0x1001cb97 → 0x100e1278  `(R) << `
- 0x1001cbbb → 0x100e1280  `\nExecution time = `
- 0x1001cbf4 → 0x100e12b0  `e:\libs\boost\boost_1_65_1\boost\log\sources\record_ostream.hpp`
- 0x1001cbf9 → 0x100e1330  `m_pStreamCompound != 0`

```c

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall
FUN_1001c810(void *this,uint param_1,uint *param_2,ushort param_3,uint *param_4,uint param_5)

{
  ushort uVar1;
  undefined1 uVar2;
  undefined1 *puVar3;
  wchar_t *pwVar4;
  undefined4 uVar5;
  void *pvVar6;
  undefined4 *puVar7;
  longlong *plVar8;
  byte ****ppppbVar9;
  char ****ppppcVar10;
  undefined2 extraout_var;
  undefined4 extraout_EDX;
  undefined2 uVar11;
  undefined4 extraout_EDX_00;
  byte ****unaff_EBX;
  char *unaff_ESI;
  bool bVar12;
  ulonglong uVar13;
  undefined4 *in_stack_fffffe90;
  int *piVar14;
  char *pcVar15;
  wchar_t *pwVar16;
  int *piVar17;
  uint uVar18;
  wchar_t *in_stack_fffffeb0;
  int *in_stack_fffffeb4;
  char *in_stack_fffffeb8;
  char *in_stack_fffffebc;
  char *in_stack_fffffec0;
  undefined4 in_stack_fffffec4;
  undefined4 in_stack_fffffec8;
  char *in_stack_fffffecc;
  int in_stack_fffffed0;
  int *in_stack_fffffed4;
  char *in_stack_fffffed8;
  undefined4 in_stack_fffffedc;
  undefined4 in_stack_fffffee0;
  undefined8 local_98;
  undefined4 local_90;
  char ***local_88 [4];
  int *local_78;
  uint local_74;
  undefined8 local_70;
  uint *local_64;
  undefined8 local_60;
  byte ***local_58 [3];
  int local_4c;
  undefined4 *local_48;
  uint local_44;
  byte ***local_40 [4];
  uint local_30;
  uint local_2c;
  int local_28;
  int local_24;
  void *local_20;
  byte ***local_1c;
  undefined1 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined1 local_8;
  undefined3 uStack_7;
  
  puStack_c = &LAB_100c3638;
  local_10 = ExceptionList;
  pwVar4 = (wchar_t *)(DAT_100fc0f4 ^ (uint)&stack0xfffffffc);
  local_14 = &stack0xfffffea0;
  ExceptionList = &local_10;
  local_60 = (ulonglong)(uint)local_60;
  local_64 = param_4;
  local_8 = 0;
  uStack_7 = 0;
  _DAT_10104db0 = (undefined2)param_1;
  DAT_10104db2 = param_3;
  _DAT_10104db4 = 0;
  local_20 = this;
  local_1c = (byte ***)pwVar4;
  puVar3 = &stack0xfffffea0;
  if ((param_3 != 0) && (puVar3 = &stack0xfffffea0, param_2 != (uint *)0x0)) {
    in_stack_fffffe90 = (undefined4 *)0x1001c88a;
    uVar13 = FUN_10093750((uint *)&DAT_10104db8,param_2,(uint)param_3);
    uVar5 = FUN_100340c0(0x10104db8,CONCAT22((short)(uVar13 >> 0x30),DAT_10104db2));
    _DAT_10104db4 = CONCAT22((short)uVar5,_DAT_10104db4);
    puVar3 = local_14;
  }
  local_14 = puVar3;
  if (*(byte *)((int)this + 0xc) < 5) {
    local_24 = 0;
    local_70 = local_70 & 0xffffffff;
    local_60 = CONCAT44((int)&local_70 + 4,(uint)local_60);
    pvVar6 = (void *)FUN_1005f320();
    FUN_10020d90(pvVar6,&local_24,(undefined4 *)((int)&local_60 + 4));
    local_8 = 1;
    while (local_24 != 0) {
      FUN_10007bd0((int *)&stack0xfffffeb0);
      local_8 = 2;
      local_98._0_4_ = FUN_1005f320();
      puVar7 = FUN_100573c0(&local_24);
      local_98._4_4_ = puVar7;
      local_90 = ___uncaught_exceptions();
      piVar14 = (int *)&stack0xfffffec0;
      _local_8 = CONCAT31(uStack_7,3);
      pcVar15 = "(W) >> ";
      uVar5 = 0x1001c93e;
      FUN_1000b420(piVar14,"(W) >> ");
      uVar18 = 0x1001c951;
      FUN_100345a0((int *)&stack0xfffffec0,(undefined2 *)&DAT_10104db0,unaff_ESI,(int *)unaff_EBX,
                   (char *)in_stack_fffffeb0,in_stack_fffffeb4,in_stack_fffffeb8,in_stack_fffffebc,
                   in_stack_fffffec0,in_stack_fffffec4,in_stack_fffffec8,in_stack_fffffecc,
                   in_stack_fffffed0,in_stack_fffffed4,in_stack_fffffed8,in_stack_fffffedc,
                   in_stack_fffffee0);
      if (puVar7 == (undefined4 *)0x0) {
        uVar18 = 0x216;
        pwVar4 = L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
        pwVar16 = L"m_pStreamCompound != 0";
        piVar14 = (int *)0x1001c969;
        FID_conflict___assert
                  (L"m_pStreamCompound != 0",
                   L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216);
        pcVar15 = (char *)pwVar16;
      }
      FUN_10007b10(&stack0xfffffeb0,&stack0xfffffe90);
      FUN_10031fd0(local_58,in_stack_fffffe90,uVar5,piVar14,pcVar15,(uint)pwVar4,uVar18);
      local_8 = 4;
      ppppbVar9 = local_58;
      if (0xf < local_44) {
        ppppbVar9 = (byte ****)local_58[0];
      }
      FUN_10031d60(local_40,(byte *)ppppbVar9,(int)local_48);
      local_8 = 3;
      uVar2 = local_8;
      local_8 = 3;
      if (0xf < local_44) {
        ppppbVar9 = (byte ****)local_58[0];
        if ((0xfff < local_44 + 1) &&
           (ppppbVar9 = (byte ****)local_58[0][-1],
           (byte *)0x1f < (byte *)((int)local_58[0] + (-4 - (int)ppppbVar9)))) {
          local_8 = uVar2;
                    /* WARNING: Subroutine does not return */
          FUN_1009cac3();
        }
        FUN_10053fdd(ppppbVar9);
      }
      local_48 = (undefined4 *)0x0;
      local_44 = 0xf;
      local_58[0] = (byte ***)((uint)local_58[0] & 0xffffff00);
      local_8 = 5;
      pwVar4 = (wchar_t *)local_40;
      if (0xf < local_2c) {
        pwVar4 = (wchar_t *)local_40[0];
      }
      FUN_1000c2f0(puVar7 + 0x18,pwVar4,local_30);
      local_8 = 3;
      uVar2 = local_8;
      local_8 = 3;
      if (0xf < local_2c) {
        unaff_EBX = (byte ****)local_40[0];
        if ((0xfff < local_2c + 1) &&
           (unaff_EBX = (byte ****)local_40[0][-1],
           (byte *)0x1f < (byte *)((int)local_40[0] + (-4 - (int)unaff_EBX)))) {
          local_8 = uVar2;
                    /* WARNING: Subroutine does not return */
          FUN_1009cac3();
        }
        unaff_ESI = (char *)0x1001ca41;
        FUN_10053fdd(unaff_EBX);
      }
      local_8 = 2;
      FUN_1001d730((int *)&local_98);
      local_8 = 1;
      in_stack_fffffeb0 =
           L"秩\xfffe웿ﱅ\xe800䙴\x02䖉趤袷\x01ༀַ䶲တ캋삃褈ꡕ桐䶰တ\xede8Ǒ樀＀ᡵ趍ｬ\xffff巨\x10樀栈縈တࢋ辉ǐ"
      ;
      FUN_10004940((int *)&stack0xfffffeb0);
    }
    local_8 = 0;
  }
  local_60 = __Xtime_get_ticks();
  pvVar6 = (void *)((int)this + 0x188);
  FUN_10039c80(pvVar6,0x10104db0,DAT_10104db2 + 8);
  plVar8 = FUN_1001db00(&local_98,param_5,0);
  *(int *)((int)this + 0x1d0) = (int)*plVar8;
  *(undefined4 *)((int)this + 0x1d4) = *(undefined4 *)((int)plVar8 + 4);
  FUN_10039cb0(pvVar6,0x10107e08,8);
  if (DAT_10107e0a != 0) {
    FUN_10039cb0(pvVar6,0x10107e10,(uint)DAT_10107e0a);
  }
  local_70 = __Xtime_get_ticks();
  FUN_10021620(&local_28,(uint *)&local_70,(uint *)&local_60);
  FUN_100217c0((double *)&local_98);
  uVar11 = extraout_var;
  if (*(byte *)((int)this + 0xc) < 5) {
    local_24 = 0;
    local_60 = local_60 & 0xffffffff;
    local_70 = CONCAT44((int)&local_60 + 4,(uint)local_70);
    pvVar6 = (void *)FUN_1005f320();
    FUN_10020d90(pvVar6,&local_24,(undefined4 *)((int)&local_70 + 4));
    local_8 = 6;
    uVar5 = extraout_EDX;
    while( true ) {
      uVar11 = (undefined2)((uint)uVar5 >> 0x10);
      if (local_24 == 0) break;
      local_70 = CONCAT44(local_98._4_4_,(int)local_98);
      FUN_10007bd0((int *)&stack0xfffffeb0);
      local_8 = 7;
      local_4c = FUN_1005f320();
      puVar7 = FUN_100573c0(&local_24);
      local_48 = puVar7;
      local_44 = ___uncaught_exceptions();
      _local_8 = CONCAT31(uStack_7,8);
      FUN_1000b420((int *)&stack0xfffffec0,"(R) << ");
      FUN_100341c0((int *)&stack0xfffffec0,&DAT_10107e08);
      piVar17 = (int *)&stack0xfffffec0;
      FUN_1000b420(piVar17,"\nExecution time = ");
      pvVar6 = (void *)FUN_100217f0(&stack0xfffffeb0,&local_70);
      pwVar4 = L"s";
      piVar14 = (int *)((int)pvVar6 + 0x10);
      uVar5 = 0x1001cbe8;
      FUN_1000b420(piVar14,"s");
      if (puVar7 == (undefined4 *)0x0) {
        in_stack_fffffeb4 = (int *)0x216;
        in_stack_fffffeb0 =
             L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp";
        pwVar4 = L"m_pStreamCompound != 0";
        piVar14 = (int *)0x1001cc03;
        FID_conflict___assert
                  (L"m_pStreamCompound != 0",
                   L"e:\\libs\\boost\\boost_1_65_1\\boost\\log\\sources\\record_ostream.hpp",0x216);
      }
      FUN_10007b10(pvVar6,&stack0xfffffea0);
      FUN_10031fd0(local_40,piVar17,uVar5,piVar14,pwVar4,(uint)in_stack_fffffeb0,
                   (uint)in_stack_fffffeb4);
      local_8 = 9;
      ppppbVar9 = local_40;
      if (0xf < local_2c) {
        ppppbVar9 = (byte ****)local_40[0];
      }
      FUN_10031d60(local_88,(byte *)ppppbVar9,local_30);
      local_8 = 8;
      uVar2 = local_8;
      local_8 = 8;
      if (0xf < local_2c) {
        ppppbVar9 = (byte ****)local_40[0];
        if ((0xfff < local_2c + 1) &&
           (ppppbVar9 = (byte ****)local_40[0][-1],
           (byte *)0x1f < (byte *)((int)local_40[0] + (-4 - (int)ppppbVar9)))) {
          local_8 = uVar2;
                    /* WARNING: Subroutine does not return */
          FUN_1009cac3();
        }
        FUN_10053fdd(ppppbVar9);
      }
      local_30 = 0;
      local_2c = 0xf;
      local_40[0] = (byte ***)((uint)local_40[0] & 0xffffff00);
      local_8 = 10;
      in_stack_fffffeb0 = (wchar_t *)local_88;
      if (0xf < local_74) {
        in_stack_fffffeb0 = (wchar_t *)local_88[0];
      }
      in_stack_fffffeb4 = local_78;
      FUN_1000c2f0(puVar7 + 0x18,in_stack_fffffeb0,(uint)local_78);
      local_8 = 8;
      uVar2 = local_8;
      local_8 = 8;
      if (0xf < local_74) {
        ppppcVar10 = (char ****)local_88[0];
        if ((0xfff < local_74 + 1) &&
           (ppppcVar10 = (char ****)local_88[0][-1],
           0x1f < (uint)((int)local_88[0] + (-4 - (int)ppppcVar10)))) {
          local_8 = uVar2;
                    /* WARNING: Subroutine does not return */
          FUN_1009cac3();
        }
        FUN_10053fdd(ppppcVar10);
      }
      local_8 = 7;
      FUN_1001d730(&local_4c);
      local_8 = 6;
      FUN_10004940((int *)&stack0xfffffeb0);
      uVar5 = extraout_EDX_00;
    }
  }
  uVar1 = DAT_10107e0a;
  if (DAT_10107e08 != param_1) {
    FUN_1001d1f8();
    return;
  }
  if (DAT_10107e0c != 0) goto switchD_1001cda9_caseD_9;
  if (DAT_10107e0a != 0) {
    uVar5 = FUN_100340c0(0x10107e10,CONCAT22(uVar11,DAT_10107e0a));
    if ((short)uVar5 != DAT_10107e0e) {
      FUN_1001d1f8();
      return;
    }
    if (local_64 == (uint *)0x0) {
      FUN_1001d1f8();
      return;
    }
    FUN_10093750(local_64,(uint *)&DAT_10107e10,(uint)uVar1);
    if (DAT_10107e0c != 0) goto switchD_1001cda9_caseD_9;
  }
  if (0xf010 < DAT_10107e08) {
    if (DAT_10107e08 != 0xf012) goto switchD_1001cda9_caseD_9;
switchD_1001cda9_caseD_c:
    bVar12 = DAT_10107e0a == 4;
    goto LAB_1001ce16;
  }
  if (DAT_10107e08 == 0xf010) {
switchD_1001cda9_caseD_4:
    bVar12 = DAT_10107e0a == 0;
    goto LAB_1001ce16;
  }
  switch(DAT_10107e08) {
  case 2:
  case 3:
    bVar12 = DAT_10107e0a == 0xc;
    break;
  case 4:
  case 5:
  case 10:
  case 0xb:
  case 0xe:
  case 0x11:
  case 0x12:
  case 0x18:
  case 0x19:
  case 0x1b:
  case 0x1c:
  case 0x23:
    goto switchD_1001cda9_caseD_4;
  case 6:
    if (DAT_10107e0a != 0) {
      if (DAT_10107e0a < 0x10) goto LAB_1001ce1d;
      if ((uint)DAT_10107e0a != DAT_10107e18 + 0x10) {
        FUN_1001d1f8();
        return;
      }
    }
    goto switchD_1001cda9_caseD_9;
  case 7:
    if ((DAT_10107e0a == 2) || (DAT_10107e0a == 3)) goto switchD_1001cda9_caseD_9;
    goto LAB_1001ce1d;
  case 8:
  case 0x20:
    bVar12 = DAT_10107e0a == 8;
    break;
  default:
    goto switchD_1001cda9_caseD_9;
  case 0xc:
  case 0xd:
  case 0x17:
  case 0x21:
    goto switchD_1001cda9_caseD_c;
  case 0x1a:
    bVar12 = DAT_10107e0a == 2;
  }
LAB_1001ce16:
  if (!bVar12) {
LAB_1001ce1d:
    FUN_1001d1f8();
    return;
  }
switchD_1001cda9_caseD_9:
  FUN_1001d1f8();
  return;
}


```


## Synthesis (2026-05-05) — the wire envelope is solved

### Architecture, end to end

```
PassThru caller
   ↓
PassThruWriteMsgs_impl (0x10005680)
   ↓ build STRUCT_MESSAGE (0x1038 bytes)
write_framer FUN_100321a0
   ↓ enqueue + Cnd_signal
write_transport FUN_1001a140         ─── push to ring buffer at channel+0x160
                                            wait for response via FUN_1001d270
[ I/O thread on the other side dequeues, formats, calls: ]
   ↓
 send_recv_transaction FUN_1001c810  ─── *** THE FRAMER ***
   ↓
write_helper FUN_10039c80 → FUN_1003bb10 (chunked)
   ↓
device_write_async FUN_1003dca0       ─── WriteFile + GetOverlappedResult
   ↓
WriteFile to \\.\COMx
```

### Wire frame (request)

`FUN_1001c810` builds the request in a global static buffer at `0x10104db0` (just an MSVC build-time-fixed scratch area, not magic):

```
+0  u16  cmd          (param_1, the J2534-internal command opcode)
+2  u16  length       (param_3, payload byte count)
+4  u16  reserved     (zero, untouched)
+6  u16  checksum     (FUN_100340c0 over payload[length])
+8  u8[length] payload
```

Total bytes written to the COM port: `length + 8`. Confirmed by `FUN_10039c80(this+0x188, 0x10104db0, DAT_10104db2 + 8)`.

### Wire frame (response)

Read into a second global static at `0x10107e08`, in two `FUN_10039cb0` calls:

```
read 8 bytes:
+0  u16  status / cmd echo
+2  u16  resp_length
+4  u16  reserved
+6  u16  expected_checksum

if resp_length != 0:
  read resp_length more bytes into payload
```

Then the validator checks the response cmd matches what was sent, computes checksum over the payload, and compares to `expected_checksum` field. Mismatch → `FUN_1001d1f8()` (error path).

### Checksum is a 16-bit byte sum

`FUN_100340c0` looks intimidating because the compiler auto-vectorized it into 16 parallel 16-bit accumulators (one per byte position in a 16-byte block), then sums them. The math reduces to:

```python
def cs16(buf):
    return sum(buf) & 0xFFFF
```

The tail loop after the unrolled vector loop handles the last `<16` bytes the same way. **Plain 16-bit additive checksum, no CRC, no XOR, no folding.** Trivial to reproduce in Kotlin.

### Per-command response-length validation table

The big switch in `FUN_1001c810` reveals expected response payload lengths per command opcode:

| cmd        | expected response length |
|------------|--------------------------|
| 2, 3       | 0x0c (12)                |
| 4, 5, 0xa, 0xb, 0xe, 0x11, 0x12, 0x18, 0x19, 0x1b, 0x1c, 0x23, 0xf010 | 0 |
| 6          | 0 OR `0x10 + payload[8..]` (variable, validated against length-stored-at-+8) |
| 7          | 2 or 3                   |
| 8, 0x20    | 8                        |
| 0xc, 0xd, 0x17, 0x21, 0xf012 | 4              |
| 0x1a       | 2                        |
| default    | accepted                 |

So at least these opcodes exist: `2, 3, 4, 5, 6, 7, 8, 0xa, 0xb, 0xc, 0xd, 0xe, 0x11, 0x12, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x20, 0x21, 0x23, 0xf010, 0xf012`. The `0x22` opcode mentioned in `write_transport` (round 3 — `FUN_1001d270(this, 0x22, msg, ...)`) doesn't appear in the validator switch, suggesting its response is variable/streamed rather than length-validated.

### Implication for the Android port

A clean-room Kotlin J2534 client can be a small piece of code:

```kotlin
fun frame(cmd: UShort, payload: ByteArray): ByteArray {
    val frame = ByteBuffer.allocate(8 + payload.size).order(LITTLE_ENDIAN)
    val sum = (payload.sumOf { it.toInt() and 0xFF }) and 0xFFFF
    frame.putShort(cmd.toShort())
    frame.putShort(payload.size.toShort())
    frame.putShort(0)                       // reserved
    frame.putShort(sum.toShort())
    frame.put(payload)
    return frame.array()
}

fun parse(reader: SerialReader): Pair<UShort, ByteArray> {
    val hdr = reader.readExactly(8)
    val status = hdr.uShort(0)
    val len    = hdr.uShort(2).toInt()
    val cs     = hdr.uShort(6).toInt()
    val body   = if (len > 0) reader.readExactly(len) else ByteArray(0)
    require((body.sumOf { it.toInt() and 0xFF } and 0xFFFF) == cs) { "checksum mismatch" }
    return status to body
}
```

Plus a command-opcode table mapping J2534 high-level operations (PassThruOpen, Connect, WriteMsgs, ReadMsgs, Ioctl) to internal opcodes 2, 3, 4, 5… that's the only part still unmapped — but the 25 opcode values are already enumerated above, and the J2534-to-opcode mapping can be derived by tracing each `PassThru*_impl` call site through to its FUN_1001d270 invocation (visible in rounds 1-3 dumps).

The risk gate "vendor-proprietary USB framing" is now fully closed — **8-byte header + payload + 16-bit byte-sum checksum, all little-endian over a USB-CDC virtual COM port at the device-driver-negotiated baud rate.** No magic constants, no signed handshake, no nonce, no clock-skew tolerance. About as friendly a wire protocol as RE'd projects come.

# CP5 Monitoring Evidence

VM: `ai-gpu-node`  
Zone: `us-central1-b`  
Thời điểm ghi nhận: `2026-08-15 03:32 UTC`  
Kênh truy cập: SSH qua IAP, không dùng public IP.

## `top`

```text
top - 03:32:19 up 12 min, 0 user, load average: 0.09, 0.10, 0.08
Tasks: 110 total, 1 running, 109 sleeping, 0 stopped, 0 zombie
%Cpu(s): 25.0 us, 50.0 sy, 0.0 ni, 25.0 id, 0.0 wa, 0.0 hi, 0.0 si, 0.0 st
MiB Mem : 3924.7 total, 2235.6 free, 510.6 used, 1430.0 buff/cache
MiB Swap: 0.0 total, 0.0 free, 0.0 used, 3414.1 avail Mem
```

## `free -h`

```text
               total        used        free      shared  buff/cache   available
Mem:           3.8Gi       508Mi       2.2Gi       544Ki       1.4Gi       3.3Gi
Swap:             0B          0B          0B
```

## `ip -s link`

```text
2: ens4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1460 state UP
    RX: bytes 325490528 packets 27590 errors 0 dropped 0
    TX: bytes 1496044 packets 14478 errors 0 dropped 0
```

Các giá trị network ở trên được đối chiếu từ ảnh chụp lệnh `ip -s link` do người
dùng cung cấp.

## Billing

```text
projectId: eng-mechanism-455017-q9
billingEnabled: true
```

Ảnh Billing Reports do người dùng cung cấp hiển thị dịch vụ `Networking`, usage
cost `đ237` và subtotal `đ0` theo khoảng thời gian hiện trên ảnh. Đây là số hiển
thị tại thời điểm chụp, không phải dự báo chi phí.

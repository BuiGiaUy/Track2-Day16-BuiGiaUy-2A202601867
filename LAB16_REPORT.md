# Lab 16 — Cloud AI Environment Report

## 1. Thông tin môi trường

- Cloud used: GCP
- Terraform source used: `terraform-gcp/`
- Project: `eng-mechanism-455017-q9`
- Region: `us-central1`
- Zone đã triển khai theo evidence: `us-central1-b` (source default là `us-central1-a`, đã override bằng `TF_VAR_zone`).
- VM đã benchmark: `ai-gpu-node`, machine type `e2-medium`.
- CPU only; `gpu_count = 0`, GPU disabled; VM đã được xác minh không có public IP trong CP3.

## 2. Terraform Infrastructure

- VPC: `ai-vpc`; private subnet: `ai-private-subnet` với CIDR `10.0.0.0/24`.
- Cloud Router `ai-router` và Cloud NAT `ai-nat` cho phép VM private tải package/dataset.
- IAP SSH qua firewall `allow-iap-ssh`; firewall `allow-lb-healthcheck` cho health check port 8000.
- Service Account `gpu-node-sa` với quyền log writer và metric writer.
- Load Balancer gồm unmanaged instance group, health check, backend service, URL map, HTTP proxy và global forwarding rule.
- Evidence lịch sử ghi nhận Terraform apply hoàn tất với 16 resources và plan sau apply là `No changes`. Tuy nhiên, read-only audit hiện tại cho thấy `terraform.tfstate` có `0 resources`, còn `terraform.tfstate.backup` có `16 resources`; cần coi đây là state anomaly, không xem là state quản lý hiện tại.

## 3. Checkpoint Summary

| Checkpoint | Mục tiêu | Trạng thái | Evidence chính |
|---|---|---|---|
| CP0 | Xác nhận GCP project, CPU mặc định, GPU tắt | PASS | Project `eng-mechanism-455017-q9`, `e2-medium`, `gpu_count=0` |
| CP1 | Chuẩn bị Terraform, gcloud, API và ADC | PASS | Terraform/gcloud/ADC đã kiểm tra |
| CP2 | Triển khai hạ tầng Terraform | PASS* | Evidence lịch sử: 16 resources, apply thành công, plan `No changes`; state hiện tại cần reconcile |
| CP3 | Private access và bootstrap | PASS | SSH qua IAP; import `lightgbm`, `sklearn`, `pandas`, `numpy` in `OK` |
| CP4 | Dataset, CPU LightGBM training và inference | FAIL* | JSON hợp lệ nhưng `evidence/benchmark.png` không khớp metric JSON |
| CP5 | Monitoring, Billing và report | PASS | `CP5_MONITORING_EVIDENCE.md`, ảnh network/Billing, report này |
| CP6 | Dọn dẹp toàn bộ tài nguyên | UNVERIFIED | Chưa có destroy evidence; audit hiện tại không tìm thấy các resource chính trên GCP |

`*` CP2, CP3 và CP5 phản ánh evidence thực thi đã ghi nhận trước audit cuối. CP4 bị FAIL ở bộ evidence hiện tại do screenshot và JSON khác nhau.

## 4. Benchmark Result

Các số liệu dưới đây lấy trực tiếp từ `benchmark_result.json`:

| Metric | Kết quả |
|---|---:|
| Dataset rows | `284807` |
| Target | `Class` |
| Training time | `3.333812707999982 seconds` |
| Accuracy | `0.998156665847407` |
| AUC | `0.9655302698597729` |
| F1 | `0.6236559139784946` |
| Precision | `0.48066298342541436` |
| Recall | `0.8877551020408163` |
| Inference latency | `0.8900440200000048 ms/row` |
| Throughput | `293741.6577353493 rows/second` |
| Inference benchmark | `1000 rows` |
| Device | `CPU` |

Configuration reproducibility: `random_state=42`, `test_size=0.2`, model `LightGBM LGBMClassifier`.

Lưu ý audit: `evidence/benchmark.png` hiển thị training `9.385635 seconds`, latency `0.857845 ms/row` và throughput `305435.56 rows/second`, khác với các giá trị trong JSON ở trên. Không dùng hai artifact này như một cặp evidence đồng bộ.

## 5. Monitoring

Evidence được ghi qua SSH IAP trên VM `ai-gpu-node`:

- CPU: `top` ghi load average `0.09, 0.10, 0.08`; CPU `25.0% user`, `50.0% system`, `25.0% idle` tại thời điểm chụp.
- RAM: tổng `3.8 GiB`, used `508 MiB`, available `3.3 GiB`; swap `0 B`.
- Network interface `ens4`: RX `325490528 bytes`, TX `1496044 bytes`.
- Network errors/drops: RX errors `0`, dropped `0`; TX errors `0`, dropped `0`.

## 6. Billing / Cost

Ảnh `evidence/billing_reports.png` là screenshot Google Cloud Billing Reports. Ảnh hiển thị dịch vụ `Networking`, usage cost `đ237` và subtotal `đ0` theo khoảng thời gian đang chọn. Không suy diễn thêm Compute Engine, Cloud NAT hoặc Load Balancing cost vì chưa có evidence cụ thể cho từng dịch vụ.

## 7. Nhận xét kết quả

1. LightGBM huấn luyện trên CPU trong `3.333812707999982` giây trên dataset `284807` dòng.
2. AUC `0.9655302698597729` cho thấy khả năng xếp hạng fraud tốt trên test set.
3. Recall `0.8877551020408163` cao hơn precision `0.48066298342541436`, nên mô hình bắt được nhiều fraud nhưng vẫn có false positive đáng kể.
4. F1 `0.6236559139784946` phản ánh sự cân bằng giữa precision và recall tốt hơn việc chỉ nhìn accuracy.
5. Inference đạt latency `0.8900440200000048 ms/row` và throughput `293741.6577353493 rows/second` trên CPU.
6. Snapshot VM cho thấy RAM còn available `3.3 GiB` và network errors/drops bằng `0`.
7. Accuracy `0.998156665847407` không đủ để đánh giá fraud detection vì dữ liệu mất cân bằng; dự đoán phần lớn giao dịch hợp lệ vẫn có thể đạt accuracy cao nhưng bỏ sót fraud.

## 8. Deliverables

- [ ] Screenshot terminal chạy `python3 benchmark.py` với toàn bộ output — `evidence/benchmark.png` có mặt nhưng metric không khớp JSON.
- [x] `benchmark_result.json` với đầy đủ metric.
- [x] Screenshot CPU/RAM/network: `evidence/network_ip_s_link.png` và evidence text.
- [x] Screenshot GCP Billing Reports: `evidence/billing_reports.png`.
- [x] Terraform source trong `terraform-gcp/`; không nộp `.terraform/` hoặc state files.
- [x] Báo cáo cuối: `LAB16_REPORT.md`.
- [ ] Evidence CP6 chạy `terraform destroy` thành công — `evidence/terraform_destroy.png` chưa hiển thị dòng `Destroy complete! Resources: 16 destroyed.`

## 9. Cleanup

Read-only audit hiện tại ghi nhận: `terraform.tfstate` có `0 resources`; `terraform.tfstate.backup` có `16 resources`; GCP không tìm thấy `ai-gpu-node`, `ai-vpc`, `ai-router`, forwarding rule hoặc `gpu-node-sa`. Ảnh destroy hiện có chỉ cho thấy plan và quá trình đang destroy, chưa có dòng hoàn tất; không kết luận CP6 PASS.

`Pending — cần xác minh nguyên nhân state/cloud discrepancy và bổ sung destroy evidence trước khi kết luận cleanup.`

# Checklist nộp bài Lab 16 — GCP

## CP4 — CPU + LightGBM

- [ ] Screenshot terminal chạy `python3 benchmark.py`, có toàn bộ output metrics.
- [ ] File `benchmark_result.json` hợp lệ, có training time, AUC, accuracy,
      precision, recall, F1, inference latency và throughput.
- [ ] Kết quả cho thấy benchmark dùng CPU; không bật GPU cho luồng bắt buộc.

## CP5 — Quan sát và báo cáo

- [ ] Screenshot CPU/RAM/network trên VM: `top`, `free -h`, `ip -s link`,
      hoặc tab Monitoring của Compute Engine.
- [ ] Screenshot GCP Billing/Cost Reports, ghi nhận các dịch vụ đang phát sinh
      chi phí nếu có.
- [ ] File `CP5_REPORT_TEMPLATE.md` đã được điền bằng số liệu thật và nhận xét
      ngắn 5–10 dòng.

## Mã nguồn và CP6

- [ ] Nộp source Terraform trong thư mục `terraform-gcp/` theo README.
- [ ] Có bằng chứng CP6 chạy `terraform destroy` thành công và kiểm tra không
      còn VM/resource đang chạy ngoài dự kiến.

## Kiểm tra bảo mật trước khi nộp

- [ ] Không lộ Kaggle API key hoặc file `kaggle.json`.
- [ ] Không lộ access token, Hugging Face token hoặc token trong terminal.
- [ ] Không nộp `.env`, credential file, private key hoặc secret khác.
- [ ] Không nộp sensitive Terraform state (`terraform.tfstate`, state backup,
      hoặc file chứa secret).
- [ ] Rà soát archive/screenshot lần cuối trước khi upload.

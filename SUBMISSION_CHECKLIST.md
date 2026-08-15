# Checklist nộp bài Lab 16 — GCP

## CP4 — CPU + LightGBM

- [ ] `evidence/benchmark.png` chứa toàn bộ output, nhưng hiện metric chưa khớp `benchmark_result.json`.
- [ ] File `benchmark_result.json` hợp lệ, có training time, AUC, accuracy,
      precision, recall, F1, inference latency và throughput.
- [ ] Kết quả cho thấy benchmark dùng CPU; không bật GPU cho luồng bắt buộc.

## CP5 — Quan sát và báo cáo

- [x] Screenshot network: `evidence/network_ip_s_link.png`.
- [x] Screenshot GCP Billing Reports: `evidence/billing_reports.png`.
- [x] Báo cáo chính toàn lab: `LAB16_REPORT.md`.

## Mã nguồn và CP6

- [ ] Nộp source Terraform trong thư mục `terraform-gcp/` theo README.
- [ ] Có bằng chứng CP6 chạy `terraform destroy` thành công với dòng
      `Destroy complete! Resources: 16 destroyed.` trong `evidence/terraform_destroy.png`.

## Kiểm tra bảo mật trước khi nộp

- [ ] Không lộ Kaggle API key hoặc file `kaggle.json`.
- [ ] Không lộ access token, Hugging Face token hoặc token trong terminal.
- [ ] Không nộp `.env`, credential file, private key hoặc secret khác.
- [ ] Không nộp sensitive Terraform state (`terraform.tfstate`, state backup,
      hoặc file chứa secret).
- [ ] Rà soát archive/screenshot lần cuối trước khi upload.

## Artifact không được nộp

- [ ] Loại `.terraform/`, `terraform.tfstate` và `terraform.tfstate.backup` khỏi archive.
- [ ] Loại `.env`, credential, Kaggle key, access token, private key và secret khác khỏi archive.

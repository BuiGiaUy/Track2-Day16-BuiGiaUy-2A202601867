# Mẫu báo cáo CP5 — Lab 16

1. Dataset `Credit Card Fraud Detection` được huấn luyện bằng LightGBM trên CPU; thời gian training: `<TRAINING_TIME> giây`.
2. AUC: `<AUC>`; accuracy: `<ACCURACY>`.
3. Precision: `<PRECISION>`; recall: `<RECALL>`; F1: `<F1>`.
4. Inference latency: `<INFERENCE_LATENCY> ms/row`; throughput: `<THROUGHPUT> rows/second`.
5. Quan sát CPU/RAM trong lúc benchmark: `<CPU_RAM_OBSERVATION>`.
6. Quan sát chi phí trên GCP Billing: `<COST_OBSERVATION>`.

Không điền số ước lượng: thay các placeholder bằng số thật trong
`benchmark_result.json` và ảnh chụp thực tế. Accuracy không đủ để đánh giá fraud
detection vì dữ liệu thường mất cân bằng; một mô hình đoán hầu hết giao dịch là
"không gian lận" vẫn có thể đạt accuracy cao nhưng bỏ sót nhiều fraud. Vì vậy cần
xem thêm AUC, precision, recall và F1.

# SLR Backend - FastAPI Application

Backend API server for the Vietnamese Sign Language Recognition system built with FastAPI, PyTorch, and ST-GCN models.

## 📋 Overview

This FastAPI application provides RESTful API endpoints for sign language recognition. It uses pre-trained ST-GCN (Spatial Temporal Graph Convolutional Network) and LSTM models to predict sign language gestures from landmark coordinates.

## 🛠 Technology Stack

- **FastAPI**: 0.110.2 - Modern, fast web framework
- **PyTorch**: For model inference
- **Uvicorn**: ASGI server
- **Python**: 3.7+
- **NumPy**: Numerical computations
- **scikit-learn**: Data preprocessing

## 📦 Prerequisites

- Python >= 3.7
- pip

## 🚀 Installation

1. **Install Python dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

   Or install from the backend directory:
   ```bash
   cd SLR_BE
   pip install fastapi uvicorn python-dotenv torch numpy scikit-learn joblib
   ```

2. **Environment Configuration**

   Create a `.env` file in the `SLR_BE` directory:
   ```env
   SLR_HOST=127.0.0.1
   SLR_PORT=8000
   SLR_ALLOW_URL=http://localhost:3000
   SLR_NUM_FRAME=30
   SLR_PREDICT_NUMBER=5
   ```

   - `SLR_HOST`: Server host address
   - `SLR_PORT`: Server port number
   - `SLR_ALLOW_URL`: CORS allowed origin (frontend URL)
   - `SLR_NUM_FRAME`: Number of frames to process
   - `SLR_PREDICT_NUMBER`: Number of predictions to return

3. **Model Files**

   Ensure the following model files are present:
   - `model/STGCN/model5_best_in_all_data.pth` - Trained ST-GCN model
   - `model/STGCN/class_mapping.txt` - Class label mappings
   - `model/STGCN/scaler.pkl` - Data scaler for preprocessing

## 💻 Usage

### Development Mode

```bash
python main.py
```

The server will start at `http://localhost:8000` (or configured host/port).

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### With Reload (Development)

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 📁 Project Structure

```
SLR_BE/
├── api/                  # API routes
│   ├── routes.py        # Main router
│   └── slr.py           # SLR-specific endpoints
├── services/            # Business logic
│   └── SLRService.py    # Sign language recognition service
├── model/               # ML models and data structures
│   ├── ai/              # Model architectures
│   │   └── LSTM_ATTENTION.py
│   ├── STGCN/           # ST-GCN model files
│   │   ├── STGCN.py
│   │   ├── graph_utils.py
│   │   ├── model5_best_in_all_data.pth
│   │   ├── class_mapping.txt
│   │   └── scaler.pkl
│   └── dto/             # Data Transfer Objects
│       ├── TestDTO.py
│       └── LandmarkPayload.py
├── utils/               # Utility functions
│   └── utils/
│       ├── LabelMapping.py
│       └── FixNumberFrame.py
├── main.py              # Application entry point
└── README.md            # This file
```

## 🔌 API Endpoints

### Health Check

- **GET** `/`
  - Returns: `"Home"`

### Test Endpoint

- **POST** `/test`
  - Request Body:
    ```json
    {
      "name": "string",
      "age": 0
    }
    ```
  - Returns: `{"age": 0, "name": "string"}`

### Sign Language Prediction

- **POST** `/api/v1/predict`
  - Request Body:
    ```json
    {
      "lm_list": [
        [x1, y1, z1, x2, y2, z2, ...],
        [x1, y1, z1, x2, y2, z2, ...],
        ...
      ]
    }
    ```
  - Returns:
    ```json
    {
      "label": "predicted_sign_label"
    }
    ```

### API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t slr-backend .
```

### Run Docker Container

```bash
docker run -p 8000:8000 --env-file .env slr-backend
```

### Using Docker Compose

See the root `docker-compose.yml` for orchestrated deployment with the frontend.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SLR_HOST` | Server host | `127.0.0.1` |
| `SLR_PORT` | Server port | `8000` |
| `SLR_ALLOW_URL` | CORS allowed origin | `http://localhost:3000` |
| `SLR_NUM_FRAME` | Number of frames to process | `30` |
| `SLR_PREDICT_NUMBER` | Number of predictions | `5` |

### Model Configuration

The service uses ST-GCN model by default. Model paths are configured in `services/SLRService.py`:

- Model path: `model/STGCN/model5_best_in_all_data.pth`
- Label mapping: `model/STGCN/class_mapping.txt`
- Scaler: `model/STGCN/scaler.pkl`

## 🧪 Testing

### Manual Testing

Use the Swagger UI at `http://localhost:8000/docs` to test endpoints interactively.

### Example cURL Request

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "lm_list": [[0.1, 0.2, 0.3, ...]]
  }'
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Model Loading Errors

- Ensure model files exist in the correct paths
- Check file permissions
- Verify PyTorch version compatibility

### CORS Issues

- Update `SLR_ALLOW_URL` in `.env` to match your frontend URL
- Ensure the frontend URL is correctly configured

### Memory Issues

- Reduce `SLR_NUM_FRAME` if processing large batches
- Use GPU if available (modify model loading in `SLRService.py`)

## 📚 Dependencies

Key dependencies (see `requirements.txt` for full list):

- `fastapi==0.110.2`
- `uvicorn==0.29.0`
- `torch` (PyTorch)
- `numpy==1.24.2`
- `scikit-learn==1.4.1.post1`
- `joblib==1.3.2`
- `python-dotenv==1.0.1`

## 🤝 Contributing

See the main project README for contributing guidelines.

## 📝 License

This project is licensed under the MIT License.


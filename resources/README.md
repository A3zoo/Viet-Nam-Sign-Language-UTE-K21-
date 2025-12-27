# SLR Frontend - React Application

Frontend application for the Vietnamese Sign Language Recognition system built with React and MediaPipe.

## 📋 Overview

This is a React-based web application that provides a user interface for real-time sign language recognition. It uses MediaPipe's Holistic solution to capture hand and pose landmarks, which are then sent to the backend API for prediction.

## 🛠 Technology Stack

- **React**: 18.3.1
- **MediaPipe**: 
  - @mediapipe/holistic
  - @mediapipe/camera_utils
  - @mediapipe/drawing_utils
- **Axios**: For API communication
- **React Scripts**: 5.0.1

## 📦 Prerequisites

- Node.js >= 14.x
- npm >= 6.x



**Configure API endpoint** (if needed)
   
   Update the API base URL in `src/api/` or environment variables if your backend runs on a different port.


## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

### API Configuration

The frontend communicates with the backend API. Ensure the backend is running and accessible at the configured URL.

## 📱 Features

- **Real-time Camera Feed**: Access and display webcam feed
- **MediaPipe Integration**: Real-time hand and pose landmark detection
- **Sign Language Recognition**: Send landmarks to backend for prediction
- **Responsive Design**: Works on desktop and mobile devices
- **Visual Feedback**: Display detected landmarks and predictions

## 🐛 Troubleshooting

### Camera Access Issues

- Ensure you're using HTTPS or localhost (required for camera access)
- Check browser permissions for camera access
- Try a different browser if issues persist

### API Connection Errors

- Verify the backend server is running
- Check the API URL configuration
- Ensure CORS is properly configured on the backend

### Build Errors

- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear npm cache: `npm cache clean --force`
- Check Node.js version compatibility

## 📚 Learn More

- [React Documentation](https://reactjs.org/)
- [MediaPipe Documentation](https://mediapipe.dev/)
- [Create React App Documentation](https://facebook.github.io/create-react-app/docs/getting-started)

## 🤝 Contributing

See the main project README for contributing guidelines.

## 📝 License

This project is licensed under the MIT License.

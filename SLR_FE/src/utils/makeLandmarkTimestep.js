const TOTAL_POSE_LANDMARKS = 25; // Số khớp trong MediaPipe Pose
const TOTAL_HAND_LANDMARKS = 21; // Số khớp trong mỗi bàn tay
const TOTAL_HANDS = 2; // Tổng số bàn tay (trái và phải)
const NOSE_POSITION = 0; // Vị trí của mũi trong danh sách Pose landmarks

// Hàm chuẩn hóa tọa độ landmarks theo vị trí mũi
export const transformToNoseCoordinate = (landmarks, noseIndex) => {
  const noseX = landmarks[noseIndex * 3];
  const noseY = landmarks[noseIndex * 3 + 1];

  return landmarks.map((value, index) => {
    if (index % 3 === 0) return value - noseX; // Chuẩn hóa x
    if (index % 3 === 1) return value - noseY; // Chuẩn hóa y
    return value; // Z và visibility không thay đổi
  });
};

// Hàm xử lý dữ liệu landmarks từ MediaPipe
export const makeLandmarkTimestep = (holisticResults) => {
  // Tạo mảng để lưu dữ liệu
  const cLm = Array(
    TOTAL_POSE_LANDMARKS * 3 + TOTAL_HAND_LANDMARKS * 3 * TOTAL_HANDS
  ).fill(0);

  // Xử lý Pose landmarks
  if (holisticResults.poseLandmarks) {
    // Chỉ lấy 25 landmarks
    holisticResults.poseLandmarks
      .slice(0, TOTAL_POSE_LANDMARKS)
      .forEach((lm, idx) => {
        cLm[idx * 3] = lm.x || 0; // X tọa độ
        cLm[idx * 3 + 1] = lm.y || 0; // Y tọa độ
        cLm[idx * 3 + 2] = lm.visibility || 0; // Độ tin cậy....
      });
  }

  // Xử lý Hand landmarks
  [
    holisticResults.leftHandLandmarks,
    holisticResults.rightHandLandmarks,
  ].forEach((handLandmarks, handIdx) => {
    if (handLandmarks) {
      // Chỉ lấy 21 landmarks
      handLandmarks.slice(0, TOTAL_HAND_LANDMARKS).forEach((lm, idx) => {
        const baseIdx =
          TOTAL_POSE_LANDMARKS * 3 +
          handIdx * TOTAL_HAND_LANDMARKS * 3 +
          idx * 3;

        cLm[baseIdx] = lm.x || 0; // X tọa độ
        cLm[baseIdx + 1] = lm.y || 0; // Y tọa độ
        cLm[baseIdx + 2] = lm.visibility || 0; // Độ tin cậy
      });
    }
  });

  // Chuẩn hóa tọa độ cLm theo vị trí mũi (khớp 0)
  const normalizedLm = transformToNoseCoordinate(cLm, NOSE_POSITION);

  return normalizedLm;
};

# 노인 활동 모니터링 시스템 설정 파일

# 기본 설정
SYSTEM_CONFIG = {
    # 카메라 설정
    'CAMERA_WIDTH': 640,
    'CAMERA_HEIGHT': 480,
    'CAMERA_FPS': 30,
    
    # MediaPipe 설정
    'MIN_DETECTION_CONFIDENCE': 0.5,
    'MIN_TRACKING_CONFIDENCE': 0.5,
    'MODEL_COMPLEXITY': 1,  # 0(라이트), 1(일반), 2(정확)
    
    # 히스토리 설정
    'POSE_HISTORY_SIZE': 300,     # 10초간 자세 데이터 (30fps)
    'ACTIVITY_HISTORY_SIZE': 1800, # 1분간 활동 데이터
    
    # 알림 설정
    'ENABLE_AUDIO_ALERTS': True,
    'ENABLE_EMAIL_ALERTS': False,  # 실제 환경에서만 사용
    'ALERT_COOLDOWN': 10,  # 중복 알림 방지 시간(초)
}

# 임계값 설정
THRESHOLDS = {
    # 낙상 감지 임계값
    'FALL_ANGLE_THRESHOLD': 60,      # 몸 기울기 각도 (도)
    'FALL_HEAD_HIP_RATIO': 1.2,     # 머리/엉덩이 높이 비율
    'FALL_SUDDEN_CHANGE': 40,       # 급격한 자세 변화 각도
    
    # 활동량 임계값
    'MOVEMENT_DETECTION': 0.01,     # 최소 움직임 감지 임계값
    'QUIET_ACTIVITY': 0.005,        # 조용한 활동 임계값
    'NORMAL_ACTIVITY': 0.02,        # 보통 활동 임계값
    'ACTIVE_THRESHOLD': 0.05,       # 활발한 활동 임계값
    
    # 시간 임계값 (초)
    'LOW_ACTIVITY_WARNING': 180,    # 3분 - 저활동 경고
    'INACTIVE_ALERT': 300,          # 5분 - 비활성 상태 알림  
    'EMERGENCY_INACTIVE': 600,      # 10분 - 응급 상황
    
    # 자세 분석 임계값
    'POSTURE_ANALYSIS_FRAMES': 90,  # 3초간 데이터로 자세 분석
    'FALL_DETECTION_FRAMES': 30,    # 1초간 데이터로 낙상 감지
}

# 응급 연락처 설정
EMERGENCY_CONTACTS = {
    'primary_family': {
        'name': '가족 (1차)',
        'phone': '+82-10-1234-5678',
        'email': 'family@example.com'
    },
    'secondary_family': {
        'name': '가족 (2차)', 
        'phone': '+82-10-1234-5679',
        'email': 'family2@example.com'
    },
    'caregiver': {
        'name': '돌봄 제공자',
        'phone': '+82-10-1234-5680', 
        'email': 'caregiver@example.com'
    },
    'emergency_service': {
        'name': '응급실',
        'phone': '119',
        'email': 'emergency@hospital.com'
    }
}

# 이메일 서버 설정 (실제 사용시 수정)
EMAIL_CONFIG = {
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': 587,
    'EMAIL_ADDRESS': 'monitoring@example.com',
    'EMAIL_PASSWORD': 'your_app_password',  # 앱 비밀번호 사용
    'USE_TLS': True
}

# 건강 상태 메시지
HEALTH_MESSAGES = {
    'EXCELLENT': {
        'ko': '✨ 우수한 활동 상태입니다!',
        'icon': '🌟',
        'color': (0, 255, 0)
    },
    'GOOD': {
        'ko': '😊 양호한 상태를 유지하고 있습니다',
        'icon': '👍', 
        'color': (0, 255, 0)
    },
    'NORMAL': {
        'ko': '🙂 평상시 활동 수준입니다',
        'icon': '👌',
        'color': (255, 255, 0)
    },
    'LOW_ACTIVITY': {
        'ko': '😐 활동량이 다소 적습니다',
        'icon': '⚠️',
        'color': (0, 165, 255)
    },
    'CONCERNING': {
        'ko': '😟 활동량이 걱정스러운 수준입니다',
        'icon': '⚠️',
        'color': (0, 100, 255) 
    },
    'ALERT': {
        'ko': '🚨 즉시 확인이 필요합니다',
        'icon': '🚨',
        'color': (0, 0, 255)
    }
}

# 활동 유형별 설정
ACTIVITY_TYPES = {
    'rest': {
        'name': '휴식 중',
        'icon': '😴',
        'color': (128, 128, 128),
        'description': '거의 움직임이 없는 상태'
    },
    'quiet': {
        'name': '조용한 활동', 
        'icon': '📖',
        'color': (255, 255, 0),
        'description': '읽기, TV 시청 등'
    },
    'normal': {
        'name': '보통 활동',
        'icon': '🚶',
        'color': (0, 255, 255), 
        'description': '일상적인 움직임'
    },
    'active': {
        'name': '활발한 활동',
        'icon': '🏃',
        'color': (0, 255, 0),
        'description': '운동, 청소 등'
    }
}

# 로그 설정
LOGGING_CONFIG = {
    'ENABLE_LOGGING': True,
    'LOG_LEVEL': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'LOG_FILE': 'elderly_monitoring.log',
    'LOG_ROTATION': True,
    'MAX_LOG_SIZE': 10 * 1024 * 1024,  # 10MB
    'LOG_BACKUP_COUNT': 5
}

# UI 설정
UI_CONFIG = {
    'WINDOW_TITLE': '노인 활동 모니터링 시스템',
    'SHOW_FPS': True,
    'SHOW_TIMESTAMP': True,
    'OVERLAY_OPACITY': 0.7,
    'INFO_PANEL_WIDTH': 400,
    'INFO_PANEL_HEIGHT': 200,
    
    # 폰트 설정
    'FONT_SCALE': 0.6,
    'FONT_THICKNESS': 2,
    'FONT_COLOR': (255, 255, 255),
    
    # 색상 설정
    'BACKGROUND_COLOR': (0, 0, 0),
    'SAFE_COLOR': (0, 255, 0),
    'WARNING_COLOR': (0, 165, 255), 
    'ALERT_COLOR': (0, 0, 255),
    'SKELETON_COLOR': (245, 117, 66),
    'CONNECTION_COLOR': (245, 66, 230)
}

# 데이터 저장 설정
DATA_CONFIG = {
    'SAVE_INTERVAL': 300,  # 5분마다 자동 저장
    'DATA_RETENTION_DAYS': 30,  # 30일간 데이터 보관
    'EXPORT_FORMAT': 'json',  # json, csv
    'BACKUP_ENABLED': True,
    'BACKUP_LOCATION': './backups/'
}

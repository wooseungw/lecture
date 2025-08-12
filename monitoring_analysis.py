"""
노인 활동 모니터링 - 데이터 분석 및 리포트 유틸리티
"""

import json
import numpy as np
from datetime import datetime, timedelta
import os
from pathlib import Path

# matplotlib은 선택적 import (없어도 기본 분석은 가능)
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️ matplotlib이 없습니다. 차트 생성은 건너뜁니다.")

# pandas는 선택적 import
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("⚠️ pandas가 없습니다. 기본 분석만 수행합니다.")

class MonitoringDataAnalyzer:
    def __init__(self, data_directory="./monitoring_data"):
        """데이터 분석기 초기화"""
        self.data_dir = Path(data_directory)
        self.data_dir.mkdir(exist_ok=True)
        
        # matplotlib 사용 가능한 경우 한글 폰트 설정
        if HAS_MATPLOTLIB:
            try:
                plt.rcParams['font.family'] = ['Arial Unicode MS', 'AppleGothic', 'Malgun Gothic']
                plt.rcParams['axes.unicode_minus'] = False
            except:
                pass
        
    def load_session_data(self, filename):
        """세션 데이터 로드"""
        try:
            with open(self.data_dir / filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"데이터 로드 실패 ({filename}): {e}")
            return None
    
    def get_all_session_files(self, days_back=7):
        """최근 N일간의 모든 세션 파일 찾기"""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        session_files = []
        
        for file_path in self.data_dir.glob("elderly_monitoring_*.json"):
            try:
                # 파일명에서 날짜 추출
                date_str = file_path.stem.split('_')[-2] + '_' + file_path.stem.split('_')[-1]
                file_date = datetime.strptime(date_str, "%Y%m%d_%H%M%S")
                
                if file_date >= cutoff_date:
                    session_files.append(file_path)
            except:
                continue
        
        return sorted(session_files)
    
    def analyze_daily_patterns(self, days_back=7):
        """일일 활동 패턴 분석"""
        session_files = self.get_all_session_files(days_back)
        daily_data = []
        
        for file_path in session_files:
            data = self.load_session_data(file_path.name)
            if data and 'daily_report' in data:
                report = data['daily_report']
                daily_data.append({
                    'date': report['date'],
                    'duration': self._parse_duration(report['monitoring_duration']),
                    'total_movement': report['total_movement_score'],
                    'avg_movement': report['average_movement'],
                    'max_movement': report['max_movement'],
                    'activity': report['current_activity'],
                    'fall_incidents': report['fall_incidents']
                })
        
        if HAS_PANDAS:
            return pd.DataFrame(daily_data)
        else:
            return daily_data  # 리스트로 반환
    
    def _parse_duration(self, duration_str):
        """시간 문자열을 분으로 변환"""
        try:
            parts = duration_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return hours * 60 + minutes + seconds / 60
        except:
            return 0
    
    def generate_activity_chart(self, data, save_path="activity_trends.png"):
        """활동량 추이 차트 생성"""
        if not HAS_MATPLOTLIB:
            print("⚠️ matplotlib이 없어 차트를 생성할 수 없습니다.")
            return None
            
        # pandas DataFrame인지 확인
        if HAS_PANDAS and hasattr(data, 'empty'):
            df = data
            if df.empty:
                print("⚠️ 차트를 생성할 데이터가 없습니다.")
                return None
        else:
            # 리스트 형태의 데이터인 경우
            if not data:
                print("⚠️ 차트를 생성할 데이터가 없습니다.")
                return None
            # 간단한 차트만 생성
            dates = [item['date'] for item in data]
            movements = [item['total_movement'] for item in data]
            
            plt.figure(figsize=(10, 6))
            plt.plot(dates, movements, marker='o')
            plt.title('일일 총 활동량 추이')
            plt.xlabel('날짜')
            plt.ylabel('활동 점수')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(save_path)
            print(f"📊 기본 차트가 저장되었습니다: {save_path}")
            return plt.gcf()
        
        # pandas DataFrame으로 상세 차트 생성
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('노인 활동 모니터링 - 주간 활동 분석', fontsize=16, fontweight='bold')
        
        # 1. 일일 총 활동량
        axes[0, 0].plot(df['date'], df['total_movement'], marker='o', color='blue', linewidth=2)
        axes[0, 0].set_title('일일 총 활동량', fontweight='bold')
        axes[0, 0].set_xlabel('날짜')
        axes[0, 0].set_ylabel('활동 점수')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 평균 활동 강도
        axes[0, 1].bar(df['date'], df['avg_movement'], color='green', alpha=0.7)
        axes[0, 1].set_title('평균 활동 강도', fontweight='bold')
        axes[0, 1].set_xlabel('날짜')
        axes[0, 1].set_ylabel('평균 움직임')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. 모니터링 시간
        axes[1, 0].bar(df['date'], df['duration'], color='orange', alpha=0.7)
        axes[1, 0].set_title('일일 모니터링 시간', fontweight='bold')
        axes[1, 0].set_xlabel('날짜')
        axes[1, 0].set_ylabel('시간 (분)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. 활동 유형 분포
        activity_counts = df['activity'].value_counts()
        axes[1, 1].pie(activity_counts.values, labels=activity_counts.index, 
                       autopct='%1.1f%%', startangle=90)
        axes[1, 1].set_title('활동 유형 분포', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"📊 상세 활동 차트가 저장되었습니다: {save_path}")
        
        return fig
    
    def generate_health_report(self, data):
        """건강 상태 리포트 생성"""
        # 데이터 타입 확인 및 변환
        if HAS_PANDAS and hasattr(data, 'empty'):
            if data.empty:
                return "분석할 데이터가 없습니다."
            df_data = data.to_dict('records')
        else:
            if not data:
                return "분석할 데이터가 없습니다."
            df_data = data
        
        # 기본 통계 계산
        avg_movements = [item['avg_movement'] for item in df_data]
        durations = [item['duration'] for item in df_data]
        fall_incidents = [item['fall_incidents'] for item in df_data]
        total_movements = [item['total_movement'] for item in df_data]
        
        avg_movement = sum(avg_movements) / len(avg_movements)
        total_monitoring_time = sum(durations)
        total_fall_incidents = sum(fall_incidents)
        max_movement_day = max(df_data, key=lambda x: x['total_movement'])
        min_movement_day = min(df_data, key=lambda x: x['total_movement'])
        
        # 활동 수준 평가
        if avg_movement >= 0.05:
            activity_level = "우수"
            activity_emoji = "🌟"
        elif avg_movement >= 0.02:
            activity_level = "양호"
            activity_emoji = "👍"
        elif avg_movement >= 0.01:
            activity_level = "보통"
            activity_emoji = "👌"
        else:
            activity_level = "주의 필요"
            activity_emoji = "⚠️"
        
        # 건강 점수 계산 (0-100)
        movement_score = min(avg_movement * 1000, 50)  # 최대 50점
        consistency_score = min(len(df_data) * 5, 30)  # 일관성, 최대 30점
        safety_score = max(20 - total_fall_incidents * 10, 0)  # 안전성, 최대 20점
        health_score = int(movement_score + consistency_score + safety_score)
        
        # 표준편차 계산
        mean_total = sum(total_movements) / len(total_movements)
        variance = sum((x - mean_total) ** 2 for x in total_movements) / len(total_movements)
        std_dev = variance ** 0.5
        
        report = f"""
🏥 노인 건강 모니터링 리포트
{'='*50}

📊 기본 통계
• 분석 기간: {len(df_data)}일간
• 총 모니터링 시간: {total_monitoring_time:.1f}분 ({total_monitoring_time/60:.1f}시간)
• 평균 일일 활동량: {avg_movement:.4f}
• 총 낙상 사고: {total_fall_incidents}회

{activity_emoji} 활동 수준: {activity_level}
🎯 건강 점수: {health_score}/100점

📈 상세 분석
• 최고 활동일: {max_movement_day['date']} ({max_movement_day['total_movement']:.4f})
• 최저 활동일: {min_movement_day['date']} ({min_movement_day['total_movement']:.4f})
• 활동량 편차: {std_dev:.4f}

💡 권장사항
"""
        
        # 개인화된 권장사항
        if avg_movement < 0.01:
            report += "• 일일 활동량을 늘리기 위해 가벼운 스트레칭이나 산책을 추천합니다.\n"
        
        if total_fall_incidents > 0:
            report += f"• 지난 주 {total_fall_incidents}회의 낙상 위험이 감지되었습니다. 환경 점검이 필요합니다.\n"
        
        if total_monitoring_time / len(df_data) < 60:
            report += "• 더 정확한 모니터링을 위해 시스템 사용 시간을 늘려보세요.\n"
        
        # 긍정적 피드백
        if health_score >= 80:
            report += "• 우수한 활동 패턴을 보이고 있습니다. 현 상태를 유지하세요! 👏\n"
        elif health_score >= 60:
            report += "• 전반적으로 양호한 상태입니다. 꾸준히 관리하세요. 😊\n"
        
        return report
    
    def export_data_to_csv(self, data, filename="monitoring_export.csv"):
        """데이터를 CSV로 내보내기"""
        try:
            csv_path = self.data_dir / filename
            
            if HAS_PANDAS and hasattr(data, 'to_csv'):
                # pandas DataFrame인 경우
                data.to_csv(csv_path, index=False, encoding='utf-8-sig')
            else:
                # 리스트 데이터인 경우 수동으로 CSV 생성
                if not data:
                    print("내보낼 데이터가 없습니다.")
                    return None
                    
                import csv
                with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
            
            print(f"📄 데이터가 CSV로 내보내졌습니다: {csv_path}")
            return csv_path
        except Exception as e:
            print(f"CSV 내보내기 실패: {e}")
            return None
    
    def cleanup_old_data(self, days_to_keep=30):
        """오래된 데이터 파일 정리"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cleaned_count = 0
        
        for file_path in self.data_dir.glob("elderly_monitoring_*.json"):
            try:
                date_str = file_path.stem.split('_')[-2] + '_' + file_path.stem.split('_')[-1]
                file_date = datetime.strptime(date_str, "%Y%m%d_%H%M%S")
                
                if file_date < cutoff_date:
                    file_path.unlink()
                    cleaned_count += 1
            except:
                continue
        
        print(f"🧹 {cleaned_count}개의 오래된 파일이 정리되었습니다.")
    
    def generate_weekly_summary(self, days_back=7):
        """주간 요약 리포트 생성"""
        data = self.analyze_daily_patterns(days_back)
        
        # 데이터 타입에 따른 빈 데이터 체크
        is_empty = False
        if HAS_PANDAS and hasattr(data, 'empty'):
            is_empty = data.empty
        else:
            is_empty = not data or len(data) == 0
        
        if is_empty:
            print("⚠️ 분석할 데이터가 없습니다.")
            return None
        
        # 차트 생성
        chart_path = f"weekly_activity_{datetime.now().strftime('%Y%m%d')}.png"
        chart_fig = None
        if HAS_MATPLOTLIB:
            chart_fig = self.generate_activity_chart(data, chart_path)
        
        # 건강 리포트 생성
        health_report = self.generate_health_report(data)
        print(health_report)
        
        # CSV 내보내기
        csv_path = f"weekly_data_{datetime.now().strftime('%Y%m%d')}.csv"
        exported_csv = self.export_data_to_csv(data, csv_path)
        
        return {
            'data': data,
            'health_report': health_report,
            'chart_path': chart_path if chart_fig else None,
            'csv_path': exported_csv
        }

def main():
    """데이터 분석 메인 함수"""
    print("🔍 노인 활동 모니터링 데이터 분석을 시작합니다...\n")
    
    analyzer = MonitoringDataAnalyzer()
    
    # 주간 요약 리포트 생성
    summary = analyzer.generate_weekly_summary(days_back=7)
    
    if summary:
        print(f"\n📊 분석 완료!")
        print(f"📈 차트 파일: {summary['chart_path']}")
        print(f"📄 데이터 파일: {summary['csv_path']}")
    
    # 오래된 데이터 정리 (30일 이상)
    analyzer.cleanup_old_data(30)
    
    print("\n✅ 데이터 분석이 완료되었습니다.")

if __name__ == "__main__":
    main()

/**
 * SlideController v1.0
 * 교육용 슬라이드 프레젠테이션 라이브러리
 * 
 * 사용법:
 * const slideController = new SlideController({
 *   slideSelector: '.slide-container',
 *   autoPlay: false,
 *   autoPlayInterval: 5000,
 *   showKeyboardGuide: true,
 *   showTimer: false
 * });
 */

/**
 * SlideController v1.0 - 향상된 버전
 */
class SlideController {
    constructor(options = {}) {
        this.config = {
            slideSelector: '.slide-container',
            autoPlay: false,
            autoPlayInterval: 0,
            showKeyboardGuide: true,
            showTimer: false,
            enableSwipe: true,
            enableKeyboard: true,
            transitionMode: 'slide',
            ...options
        };
        
        this.slides = [];
        this.currentSlide = 0;
        this.totalSlides = 0;
        this.autoPlayTimer = null;
        this.touchStartX = 0;
        this.touchEndX = 0;
        
        this.init();
    }
    
    init() {
        this.slides = document.querySelectorAll(this.config.slideSelector);
        this.totalSlides = this.slides.length;
        
        if (this.totalSlides === 0) {
            console.warn('SlideController: 슬라이드를 찾을 수 없습니다.');
            return;
        }
        
        this.setupSlides();
        this.createControlUI();
        this.bindEvents();
        this.updateUI();
        
        if (this.config.showKeyboardGuide) {
            this.createKeyboardGuide();
        }
        
        document.body.classList.add('slide-mode');
        console.log(`SlideController 초기화 완료: ${this.totalSlides}개 슬라이드`);
    }
    
    setupSlides() {
        this.slides.forEach((slide, index) => {
            slide.classList.remove('active', 'prev', 'next');
            if (index === 0) {
                slide.classList.add('active');
            }
        });
    }
    
    createControlUI() {
        this.removeExistingUI();
        this.createProgressBar();
        this.createControlPanel();
    }
    
    removeExistingUI() {
        const existingElements = ['.slide-progress', '.slide-controls', '.keyboard-guide'];
        existingElements.forEach(selector => {
            // 여러 개의 중복 요소들을 모두 제거
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (element) element.remove();
            });
        });
        
        // body에서 slide-mode 클래스 제거 후 다시 추가 (초기화)
        document.body.classList.remove('slide-mode');
    }
    
    createProgressBar() {
        const progressBar = document.createElement('div');
        progressBar.className = 'slide-progress';
        progressBar.id = 'slideProgressBar';
        document.body.appendChild(progressBar);
    }
    
    createControlPanel() {
        const controlPanel = document.createElement('div');
        controlPanel.className = 'slide-controls';
        controlPanel.innerHTML = `
            <button class="control-btn" id="slidePrevBtn" title="이전 슬라이드 (←)">
                <i class="fas fa-chevron-left"></i>
            </button>
            <div class="slide-indicator" id="slideIndicator">
                ${this.createIndicatorDots()}
            </div>
            <span class="slide-number" id="slideNumber">${this.currentSlide + 1} / ${this.totalSlides}</span>
            <button class="control-btn" id="slideNextBtn" title="다음 슬라이드 (→)">
                <i class="fas fa-chevron-right"></i>
            </button>
            <button class="control-btn" id="slideFullscreenBtn" title="전체화면 (F11)">
                <i class="fas fa-expand"></i>
            </button>
        `;
        document.body.appendChild(controlPanel);
    }
    
    createIndicatorDots() {
        let dots = '';
        for (let i = 0; i < this.totalSlides; i++) {
            const activeClass = i === 0 ? ' active' : '';
            dots += `<div class="indicator-dot${activeClass}" data-slide="${i}"></div>`;
        }
        return dots;
    }
    
    createKeyboardGuide() {
        const guide = document.createElement('div');
        guide.className = 'keyboard-guide';
        guide.innerHTML = `
            <h4>키보드 단축키</h4>
            <div><kbd>←</kbd> <kbd>→</kbd> 슬라이드 이동</div>
            <div><kbd>Space</kbd> 다음 슬라이드</div>
            <div><kbd>Home</kbd> 첫 슬라이드</div>
            <div><kbd>End</kbd> 마지막 슬라이드</div>
            <div><kbd>F11</kbd> 전체화면</div>
        `;
        document.body.appendChild(guide);
        
        setTimeout(() => {
            guide.classList.add('hidden');
        }, 0);
    }
    
    bindEvents() {
        this.bindButtonEvents();
        
        if (this.config.enableKeyboard) {
            this.bindKeyboardEvents();
        }
        
        if (this.config.enableSwipe) {
            this.bindTouchEvents();
        }
        
        this.bindIndicatorEvents();
        this.bindFullscreenEvents();
    }
    
    bindButtonEvents() {
        const prevBtn = document.getElementById('slidePrevBtn');
        const nextBtn = document.getElementById('slideNextBtn');
        const fullscreenBtn = document.getElementById('slideFullscreenBtn');
        
        if (prevBtn) prevBtn.addEventListener('click', () => this.prevSlide());
        if (nextBtn) nextBtn.addEventListener('click', () => this.nextSlide());
        if (fullscreenBtn) fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
    }
    
    bindKeyboardEvents() {
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    this.prevSlide();
                    break;
                case 'ArrowRight':
                case ' ':
                    e.preventDefault();
                    this.nextSlide();
                    break;
                case 'Home':
                    e.preventDefault();
                    this.goToSlide(0);
                    break;
                case 'End':
                    e.preventDefault();
                    this.goToSlide(this.totalSlides - 1);
                    break;
                case 'F11':
                    e.preventDefault();
                    this.toggleFullscreen();
                    break;
            }
        });
    }
    
    bindTouchEvents() {
        document.addEventListener('touchstart', (e) => {
            this.touchStartX = e.touches[0].clientX;
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            this.touchEndX = e.changedTouches[0].clientX;
            const deltaX = this.touchStartX - this.touchEndX;
            
            if (Math.abs(deltaX) > 50) {
                if (deltaX > 0) {
                    this.nextSlide();
                } else {
                    this.prevSlide();
                }
            }
        }, { passive: true });
    }
    
    bindIndicatorEvents() {
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('indicator-dot')) {
                const slideIndex = parseInt(e.target.dataset.slide);
                this.goToSlide(slideIndex);
            }
        });
    }
    
    bindFullscreenEvents() {
        // 전체화면 상태 변경 이벤트 리스너들
        document.addEventListener('fullscreenchange', () => this.handleFullscreenChange());
        document.addEventListener('webkitfullscreenchange', () => this.handleFullscreenChange());
        document.addEventListener('mozfullscreenchange', () => this.handleFullscreenChange());
        document.addEventListener('MSFullscreenChange', () => this.handleFullscreenChange());
    }
    
    handleFullscreenChange() {
        const isFullscreen = !!(document.fullscreenElement || 
                                document.webkitFullscreenElement || 
                                document.mozFullScreenElement || 
                                document.msFullscreenElement);
        
        const controls = document.querySelector('.slide-controls');
        const progressBar = document.querySelector('.slide-progress');
        
        if (isFullscreen) {
            // 전체화면일 때 컨트롤러 숨기기
            if (controls) controls.style.display = 'none';
            if (progressBar) progressBar.style.display = 'none';
            console.log('전체화면 진입: 컨트롤러 숨김');
        } else {
            // 전체화면 해제 시 컨트롤러 다시 표시
            if (controls) controls.style.display = 'flex';
            if (progressBar) progressBar.style.display = 'block';
            console.log('전체화면 해제: 컨트롤러 표시');
        }
    }
    
    goToSlide(index) {
        if (index < 0 || index >= this.totalSlides || index === this.currentSlide) return;
        
        this.slides[this.currentSlide].classList.remove('active');
        this.currentSlide = index;
        this.slides[this.currentSlide].classList.add('active');
        
        this.slides.forEach((slide, i) => {
            if (i !== this.currentSlide) {
                slide.classList.remove('active');
            }
        });
        
        this.updateUI();
    }
    
    nextSlide() {
        if (this.currentSlide < this.totalSlides - 1) {
            this.goToSlide(this.currentSlide + 1);
        }
    }
    
    prevSlide() {
        if (this.currentSlide > 0) {
            this.goToSlide(this.currentSlide - 1);
        }
    }
    
    updateUI() {
        const prevBtn = document.getElementById('slidePrevBtn');
        const nextBtn = document.getElementById('slideNextBtn');
        const slideNumber = document.getElementById('slideNumber');
        const progressBar = document.getElementById('slideProgressBar');
        
        if (prevBtn) prevBtn.disabled = this.currentSlide === 0;
        if (nextBtn) nextBtn.disabled = this.currentSlide === this.totalSlides - 1;
        
        if (slideNumber) {
            slideNumber.textContent = `${this.currentSlide + 1} / ${this.totalSlides}`;
        }
        
        document.querySelectorAll('.indicator-dot').forEach((dot, i) => {
            dot.classList.toggle('active', i === this.currentSlide);
        });
        
        if (progressBar) {
            const progress = ((this.currentSlide + 1) / this.totalSlides) * 100;
            progressBar.style.width = `${progress}%`;
        }
    }
    
    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.log('전체화면 진입 실패:', err);
            });
        } else {
            document.exitFullscreen();
        }
    }
}

// 전역에서 사용 가능하도록 설정
window.SlideController = SlideController;

// 중복 초기화 방지를 위한 변수
let slideControllerInitialized = false;

// 페이지 로드 후 자동 초기화
document.addEventListener('DOMContentLoaded', function() {
    // 이미 초기화되었다면 실행하지 않음
    if (slideControllerInitialized) {
        console.log('SlideController 이미 초기화됨');
        return;
    }
    
    // 기존 인스턴스가 있다면 제거
    if (window.slideController) {
        console.log('기존 SlideController 인스턴스 정리');
        window.slideController = null;
    }
    
    // 기존 UI 요소들 정리
    const elementsToRemove = ['.slide-progress', '.slide-controls', '.keyboard-guide'];
    elementsToRemove.forEach(selector => {
        const element = document.querySelector(selector);
        if (element) {
            element.remove();
        }
    });
    
    // 새로운 인스턴스 생성
    window.slideController = new SlideController({
        slideSelector: '.slide-container',
        showKeyboardGuide: false,
        enableSwipe: true,
        enableKeyboard: true
    });
    
    slideControllerInitialized = true;
    console.log('SlideController 초기화 완료');
});
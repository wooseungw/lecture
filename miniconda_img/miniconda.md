# 미니콘다(Miniconda3) 설치 및 가상환경 생성 가이드

## 1. Miniconda 다운로드

- [Miniconda 공식 다운로드 페이지](https://www.anaconda.com/download/success)에 접속합니다.
- 자신의 운영체제(Windows, Mac)에 맞는 설치 파일을 다운로드합니다.
- **Miniconda Installers** 다운로드 버튼을 클릭합니다.  
    ![다운로드](miniconda_img/miniconda_down.png)  
    <sub>※ 예시 이미지는 Mac 환경입니다. 각 운영체제에 맞는 버튼을 선택하세요.</sub>


---

## 2. Miniconda 설치

- **Mac**
    - 다운로드한 파일을 더블 클릭하여 설치를 시작합니다.
- **Windows**
    - 다운로드한 파일을 우클릭 → **관리자 권한으로 실행**을 선택합니다.

설치 과정에서  
- <em>이 컴퓨터의 모든 사용자를 위해 설치를</em> 선택합니다.
- **Path 환경변수 설정** 창이 뜨면 **예**를 선택합니다.

    ![설치1](miniconda_img/install1.png)
    ![설치2](miniconda_img/install2.png)
    ![설치3](miniconda_img/install3.png)

<sub>출처: https://swmakerjun.tistory.com/80</sub>

---

## 3. 설치 확인

- 설치가 완료되면 아래 폴더가 생성됩니다.
    - **Mac:** `~/Miniconda3`
    - **Windows:** `C:\ProgramData\Miniconda3`

---

## 4. Miniconda 환경 초기화

### Mac

1. **터미널** 또는 **iTerm2** 실행
2. 아래 명령어 입력:
        ```bash
        conda init
        ```
3. 셸 종류에 따라 명시적으로 입력할 수도 있습니다:
        ```bash
        conda init zsh   # zsh 사용 시
        conda init bash  # bash 사용 시
        ```
4. 초기화 후 터미널을 재시작하거나 아래 명령어로 적용:
        ```bash
        source ~/.zshrc   # zsh 사용 시
        source ~/.bashrc  # bash 사용 시
        ```

### Windows

1. **시작** → **Anaconda Prompt**를 관리자 권한으로 실행
2. 아래 명령어 입력:
        ```bash
        conda init
        ```
3. 초기화가 완료되면 프롬프트를 닫았다가 다시 실행합니다.

> `conda init` 명령어는 conda를 모든 터미널에서 사용할 수 있도록 환경설정을 자동으로 추가합니다.  
> *init*은 *initialization*의 약어입니다.

---

## 5. 가상환경 생성 및 활성화

### 가상환경 생성

```bash
conda create -n [가상환경이름] python=[파이썬버전]
```
- 예시:  
    ```bash
    conda create -n action python=3.12
    ```
    → "action"이라는 이름의 가상환경에 Python 3.12 설치
- 가상환경 생성 후 아래와 같은 메시지가 출력됩니다:
    ```
    Proceed ([y]/n)? 
    ```
- **y**를 입력하여 설치를 진행합니다.
### 가상환경 활성화

```bash
conda activate [가상환경이름]
```
- 예시:  
    ```bash
    conda activate action
    ```

---

## 6. 패키지 설치

가상환경이 활성화된 상태에서 필요한 패키지를 설치합니다.

- 예시: OpenCV 설치
    ```bash
    pip install opencv-python
    ```

- 설치된 패키지 목록 확인:
    ```bash
    pip list
    ```
---

## 7. 내 가상환경으로 VSCode에서 파이썬 실행하기
1. **VSCode**를 실행합니다.
2. Ctrl + Shift + P를 눌러 **명령 팔레트**를 엽니다.
3. `Python: Select Interpreter`를 입력하고 선택합니다.
4. 목록에서 방금 생성한 가상환경을 선택합니다. (예: `action`)
5. 이제 VSCode에서 해당 가상환경을 사용하여 파이썬 코드를 실행할 수 있습니다.

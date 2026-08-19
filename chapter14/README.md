# chapter14 (번역서 13장) 실행 안내

『Data Pipelines with Apache Airflow, Second Edition』 번역서 13장(생성형 AI 프로젝트)의 예제 코드입니다.

0) 프로젝트 디렉터리로 이동합니다.
    `cd chapter14`

1) Docker Compose 파일을 실행합니다.
    `docker compose up -d`

2) MinIO가 뜨면 다음 자격 증명으로 `http://localhost:8083` 의 MinIO 웹 인터페이스에 접근할 수 있습니다.
    - Access Key: `airflow`
    - Pass: `apacheairflow`

3) 장 폴더에 있는 `.env.template` 파일 내용을 `.env` 라는 새 파일로 복사합니다.

4) MinIO UI에서 액세스 키를 만들고, 이 저장소의 `.env` 파일에서 다음 변수를 갱신합니다.
    ```
    * MINIO_ID
    * MINIO_KEY
    ```
    만든 id와 key를 `.env` 파일의 다음 변수에 넣습니다.
    ```
    AWS_ACCESS_KEY_ID=MINIO_ID
    AWS_SECRET_ACCESS_KEY=MINIO_KEY
    ```
5) OpenAI API 키를 `.env` 파일에 추가합니다.

    a) OpenAI API는 계정을 만들고 OpenAI 웹사이트에서 API 키를 받아야 합니다.
        ```
        OPENAI_API_KEY=45dw2354910a454gf2ba90f3f238EXAMPLE
        ```

    b) Azure OpenAI는 Azure에서 텍스트 임베딩 리소스를 만들고, Azure 포털에서 API 키와 엔드포인트를 받아 `.env` 파일에 다음 변수를 추가합니다.

        ```
        OPENAI_API_KEY=45dw2354910a454gf2ba90f3f238EXAMPLE
        AZURE_OPENAI_RESOURCE_NAME=project-openai-nl
        AZURE_OPENAI_ENDPOINT=https://project-openai-nl.openai.azure.com/
        ```
6) docker compose를 멈췄다가(ctrl+c) 변경 사항이 반영되도록 다시 실행합니다.
    `docker compose up  -d --build`

7) Airflow에서 DAG를 실행합니다.

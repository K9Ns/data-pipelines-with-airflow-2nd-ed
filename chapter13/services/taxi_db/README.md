# Taxi DB

이 디렉터리의 Dockerfile은 2023년 NYC 옐로 택시 데이터를 담은 Postgres DB를 빌드합니다. 데이터 세트가 커서 Docker 이미지가 매우 커지므로, 입력 데이터에서 X번째 줄마다 하나씩만 골라 이미지를 약 1GB로 맞췄습니다.

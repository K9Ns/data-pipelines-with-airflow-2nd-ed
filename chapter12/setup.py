import setuptools

setuptools.setup(
    name="nyctransport",
    version="0.1",
    description="NYC 교통 프로젝트용 커스텀 Airflow 구성요소를 담은 패키지.",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["apache-airflow~=3.1"],
    python_requires=">=3.12",
)

# **wanted-pre-onboarding-backend**

이름: 김대영

## 1. 기본 사항

### 1.1. 목적
이번 프로젝트는 게시판을 관리하는 웹 백엔드 프로그램을 만드는 것을 목적으로 한다.

### 1.2. 사용된 기술
이번 프로젝트에 사용된 기술 및 모듈은 다음과 같다.
- git: 분산 버전 관리 시스템. 프로젝트에 포함된 파일들을 관리하기 위해서 사용됨

- docker: 컨테이너 기술. python과 mysql등 많은 프로그램들이 도커 이미지로 만들어져 있어 필요한 프로그램을 가져올 수 있으며, 손쉽게 인프라를 구축할 수 있어 채택

- mysql: 데이터베이스 관리 시스템. 서버로 들어오는 데이터를 저장하기 위해서 사용됨

- python: 이번 프로젝트에 사용된 메인 프로그래밍 언어.
    - flask: 서버 개발에 사용된 모듈. 다른 웹 서버용 프레임워크에 비해 간결하기에 채택

### 1.3. 환경 설정
다음과 같은 프로그램을 설치하여야 한다.
- git
- docker desktop

또한 이번 프로젝트는 Windows 10 환경에서 제작되었음을 밝힌다.

## 2. 실행 방법
1. 콘솔 화면에 다음 명령어를 입력하여 git repository를 clone한다.

    > git clone https://github.com/kdyst/wanted-pre-onboarding-backend.git

<br>

2. 실행 결과 생성된 폴더로 들어간다.

<br>

3. 다음 명령어를 실행하면 프로그램이 실행된다.

    > docker-compose up -d

<br>

4. 실행된 프로그램은 5000번 포트를 통해 접근할 수 있다.

    > localhost:5000/etc...

<br>

5. 프로그램을 종료하기 전에 데이터베이스를 저장하고 싶다면 다음 명령어를 입력한다.

    > docker exec -it database /usr/bin/mysqldump -u root --password=root community > backup.sql

    5.1. 혹시라도 데이터베이스 컨테이너가 작동을 멈춘 경우 위 명령어가 통하지 않는다. 다음과 같이 조치할 것.

    > docker ps -a
    >
    > 비활성화된 컨테이너를 확인할 수 있는 명령어
    >
    > 위 명령어를 치고 database가 있는지 확인한다.

    > docker start database
    >
    > 위 명령을 통해 컨테이너를 활성화하면 된다.

<br>

6. 프로그램을 종료하려면 다음 명령어를 순서대로 입력한다.

    > docker-compose down
    >
    > 모든 컨테이너를 멈추고, 삭제한다.

    > docker images
    >
    > 도커 이미지들을 확인할 수 있는 명령어
    >
    > 위에서 backend와 mysql 이미지를 확인할 수 있다.

    > docker rmi $(이미지 이름: backend 혹은 mysql:8.0)
    >
    > "docker images"에서 확인할 수 있는 이미지를 지우는 명령어

<br>

## 2.1. 엔드포인트 호출 방법(API)

위의 프로그램 실행 이후 5000번 포트에 접속해서 다음과 같은 상호작용이 가능하다.

> 참고: 아래의 URL 중 <...>은 URL에서 받는 변수를 의미한다.
>
> 예) localhost:5000/api/content/< int:post_id >
>
>   localhost:5000/api/content/3
>
>   --> post_id == 3

- 회원가입

    사용자의 이메일을 ID로 사용한다. 만약 이메일과 비밀번호의 조건이 맞지 않거나, 해당 이메일을 이미 사용하고 있다면 Fail을 받게 된다. 성공시 새로운 계정이 생성된다.
    <table>
        <tr>
            <th> URL </th>
            <th> localhost:5000/api/auth/sign-up </th>
        </tr>
        <tr>
            <th> METHOD </th>
            <th> POST </th>
        </tr>
        <tr>
            <th> REQUEST BODY </th>
            <th>
                <table>
                    <tr>
                        <th> email </th>
                        <th> 이메일 주소 </th>
                    </tr>
                    <tr>
                        <th> password </th>
                        <th> 비밀번호 </th>
                    </tr>
                </table>
            </th>
        </tr>
        <tr>
            <th> RESPONSE BODY </th>
            <th>
                <table>
                    <tr>
                        <th> status </th>
                        <th>
                            성공 시 "Success"<br>
                            실패 시 "Fail" 
                        </th>
                    </tr>
                </table>
            </th>
        </tr>
    </table>

<br>

- 로그인
    사용자의 이메일을 ID로 사용한다. 만약 이메일과 비밀번호의 조건이 맞지 않거나, 해당 이메일을 사용한 사람이 없거나, 해당 이메일에 연결된 비밀번호가 다르다면 Fail을 출력한다. 성공시 JWT 토큰을 발행한다.
    <table>
        <tr>
            <th> URL </th>
            <th> localhost:5000/api/auth/sign-in </th>
        </tr>
        <tr>
            <th> METHOD </th>
            <th> POST </th>
        </tr>
        <tr>
            <th> REQUEST BODY </th>
            <th>
                <table>
                    <tr>
                        <th> email </th>
                        <th> 이메일 주소 </th>
                    </tr>
                    <tr>
                        <th> password </th>
                        <th> 비밀번호 </th>
                    </tr>
                </table>
            </th>
        </tr>
        <tr>
            <th> RESPONSE BODY </th>
            <th>
                <table>
                    <tr>
                        <th> status </th>
                        <th>
                            성공 시 "Success"<br>
                            실패 시 "Fail" 
                        </th>
                    </tr>
                    <tr>
                        <th> JWT </th>
                        <th> JWT 토큰 </th>
                    </tr>
                </table>
            </th>
        </tr>
    </table>

<br>

- 게시글 생성
    미리 생성한 JWT 토큰을 필요로 하며, 각 게시글은 제목과 내용에 해당하는 문자열을 가지도록 만들었다. JWT 토큰을 가지고 있고, REQUEST BODY를 누락하지 않았다면 새로운 게시글을 출력할 것이다.

    <table>
        <tr>
            <th> URL </th>
            <th> localhost:5000/api/content/new </th>
        </tr>
        <tr>
            <th> METHOD </th>
            <th> POST </th>
        </tr>
        <tr>
            <th> REQUEST BODY </th>
            <th>
                <table>
                    <tr>
                        <th> title </th>
                        <th> 게시글 제목 </th>
                    </tr>
                    <tr>
                        <th> content </th>
                        <th> 글 내용 </th>
                    </tr>
                </table>
            </th>
        </tr>
        <tr>
            <th> RESPONSE BODY </th>
            <th>
                <table>
                    <tr>
                        <th> status </th>
                        <th>
                            성공 시 "Success"<br>
                            실패 시 "Fail" 
                        </th>
                    </tr>
                </table>
            </th>
        </tr>
    </table>

<br>

- 총 페이지의 수
    이번 과제에서 pagination은 두 부분으로 이루어져 있다. 이것은 페이지 당 게시글 수를 기반으로 페이지의 수를 계산하는 엔드포인트이다.

    <table>
        <tr>
            <th> URL </th>
            <th> localhost:5000/api/content/pages/&lt int:unit &gt </th>
        </tr>
        <tr>
            <th> METHOD </th>
            <th> GET </th>
        </tr>
        <tr>
            <th> VARIABLE </th>
            <th>
                <table>
                    <tr>
                        <th> unit </th>
                        <th> 페이지 당 게시글 수 </th>
                    </tr>
                </table>
            </th>
        </tr>
        <tr>
            <th> RESPONSE BODY </th>
            <th>
                <table>
                    <tr>
                        <th> status </th>
                        <th>
                            성공 시 "Success"<br>
                            실패 시 "Fail" 
                        </th>
                    </tr>
                    <tr>
                        <th> num </th>
                        <th> 페이지의 개수 </th>
                    </tr>
                </table>
            </th>
        </tr>
    </table>

<br>

- 게시글 목록
    이 부분은 실제 pagination에 해당하는 부분이다. 페이지 당 글의 개수, 그리고 페이지의 인덱스(1부터 시작)을 받으면 실제 게시글의 ID, 게시자, 그리고 제목을 얻을 수 있다. 다만 게시글의 내용은 pagination에서 보여주지 않고 실제 게시글을 보아야 확인할 수 있게 만들었다.

    <table>
        <tr>
            <th> URL </th>
            <th> localhost:5000/api/content/pages/&lt int:unit &gt/ &lt int:page_id &gt </th>
        </tr>
        <tr>
            <th> METHOD </th>
            <th> GET </th>
        </tr>
        <tr>
            <th> VARIABLE </th>
            <th>
                <table>
                    <tr>
                        <th> unit </th>
                        <th> 페이지 당 게시글 수 </th>
                    </tr>
                    <tr>
                        <th> page_id </th>
                        <th> 페이지 인덱스 </th>
                    </tr>
                </table>
            </th>
        </tr>
        <tr>
            <th> RESPONSE BODY </th>
            <th>
                <table>
                    <tr>
                        <th> status </th>
                        <th>
                            성공 시 "Success"<br>
                            실패 시 "Fail" 
                        </th>
                    </tr>
                    <tr>
                        <th> posts </th>
                        <th>
                            <table>
                                <caption>게시글 목록</caption>
                                <tr>
                                    <th>post_id</th>
                                    <th>게시글의 ID</th>
                                </tr>
                                <tr>
                                    <th>user_id</th>
                                    <th>게시자</th>
                                </tr>
                                <tr>
                                    <th>title</th>
                                    <th>게시글의 제목</th>
                                </tr>
                            </table>
                        </th>
                    </tr>
                </table>
            </th>
        </tr>
    </table>

<br>

- 게시글 조회
    위에서 얻은 post_id를 이용하면 게시글을 조회할 수 있게 된다. 또한 게시글의 내용을 확인할 수 있다.

    <table>
        <tr>
            <th> URL </th>
            <th> localhost:5000/api/content/&lt int:post_id &gt </th>
        </tr>
        <tr>
            <th> METHOD </th>
            <th> GET </th>
        </tr>
        <tr>
            <th> VARIABLE </th>
            <th>
                <table>
                    <tr>
                        <th> post_id </th>
                        <th> 게시글의 ID </th>
                    </tr>
                </table>
            </th>
        </tr>
        <tr>
            <th> RESPONSE BODY </th>
            <th>
                <table>
                    <tr>
                        <th> status </th>
                        <th>
                            성공 시 "Success"<br>
                            실패 시 "Fail" 
                        </th>
                    </tr>
                    <tr>
                        <th> author </th>
                        <th> 게시자 </th>
                    </tr>
                    <tr>
                        <th> title </th>
                        <th> 제목 </th>
                    </tr>
                    <tr>
                        <th> content </th>
                        <th> 내용 </th>
                    </tr>
                </table>
            </th>
        </tr>
    </table>

<br>

- 게시글 수정
    앞서 설명한 JWT를 이용해서 게시글을 수정하는 사람이 게시글의 주인인지 확인한다. 게시글을 수정할 때는 제목이나 내용을 새로 전송하면 된다. 게시글이 존재하고 수정하는 사람이 같다면 성공한다.

    <table>
        <tr>
            <th> URL </th>
            <th> localhost:5000/api/content/&lt int:post_id &gt </th>
        </tr>
        <tr>
            <th> METHOD </th>
            <th> PATCH </th>
        </tr>
        <tr>
            <th> VARIABLE </th>
            <th>
                <table>
                    <tr>
                        <th> post_id </th>
                        <th> 게시글의 ID </th>
                    </tr>
                </table>
            </th>
        </tr>
        <tr>
            <th> REQUEST BODY </th>
            <th>
                <table>
                    <tr>
                        <th> title </th>
                        <th> 게시글 제목(option) </th>
                    </tr>
                    <tr>
                        <th> content </th>
                        <th> 글 내용(option) </th>
                    </tr>
                </table>
            </th>
        </tr>
        <tr>
            <th> RESPONSE BODY </th>
            <th>
                <table>
                    <tr>
                        <th> status </th>
                        <th>
                            성공 시 "Success"<br>
                            실패 시 "Fail" 
                        </th>
                    </tr>
                </table>
            </th>
        </tr>
    </table>

<br>

- 게시글 삭제
    앞서 설명한 JWT를 이용해서 게시글을 삭제하는 사람이 게시글의 주인인지 확인한다. 게시글이 존재하고 게시글의 주인과 삭제하려는 사람이 달라야만 실패한다. 이 이후에는 해당 글이 존재하지 않게 된다.

    <table>
        <tr>
            <th> URL </th>
            <th> localhost:5000/api/content/&lt int:post_id &gt </th>
        </tr>
        <tr>
            <th> METHOD </th>
            <th> DELETE </th>
        </tr>
        <tr>
            <th> VARIABLE </th>
            <th>
                <table>
                    <tr>
                        <th> post_id </th>
                        <th> 게시글의 ID </th>
                    </tr>
                </table>
            </th>
        </tr>
        <tr>
            <th> RESPONSE BODY </th>
            <th>
                <table>
                    <tr>
                        <th> status </th>
                        <th>
                            성공 시 "Success"<br>
                            실패 시 "Fail" 
                        </th>
                    </tr>
                </table>
            </th>
        </tr>
    </table>

<br>

## 3. 데이터베이스 테이블 구조
이번 프로젝트에서 구성한 데이터베이스의 구조는 다음과 같다.

<table>
<caption> user_table
    <tr>
        <th>(PK) user_id</th>
        <th>varchar(255) not null</th>
    </tr>
    <tr>
        <th>password</th>
        <th>binary(60)</th>
    </tr>
<table>
- 사용자의 ID(이메일)를 암호화된 비밀번호와 대응시키는 테이블.

<br>

<table>
<caption> post_table
    <tr>
        <th>(PK) post_id</th>
        <th>int auto increment not null</th>
    </tr>
    <tr>
        <th>(FK) user_id</th>
        <th>varchar(255) not null</th>
    </tr>
    <tr>
        <th>title</th>
        <th>varchar(255)</th>
    </tr>
    <tr>
        <th>content</th>
        <th>text</th>
    </tr>
<table>
- 게시글을 관리하는 테이블. 각 게시글은 고유한 번호, 게시자, 제목, 그리고 글 내용을 가지고 있다.


## 4. 실행 영상

# <a href = "https://youtu.be/0t1aDRkmUyQ">CLICK</a>
step 1: Clone the project and make a virtual environment
        Commands for creating virtual environment are given:
        python3 -m venv venv
        source venv/bin/activate

step 2:  libraries use in this project:
          asgiref==3.8.1
          attrs==24.2.0
          backports.zoneinfo==0.2.1
          cattrs==24.1.2
          certifi==2024.8.30
          charset-normalizer==3.4.0
          Django==4.2.16
          djangorestframework==3.15.2
          djangorestframework-simplejwt==5.3.1
          exceptiongroup==1.2.2
          flatbuffers==24.3.25
          idna==3.10
          numpy==1.24.4
          openmeteo-requests==1.3.0
          openmeteo-sdk==1.18.0
          pandas==2.0.3
          platformdirs==4.3.6
          PyJWT==2.9.0
          python-dateutil==2.9.0.post0
          pytz==2024.2
          requests==2.32.3
          requests-cache==1.2.1
          retry-requests==2.0.0
          six==1.16.0
          sqlparse==0.5.2
          typing-extensions==4.12.2
          tzdata==2024.2
          url-normalize==1.4.3
          urllib3==2.2.3

          use pip install -r requirements.txt to install this 
          
step 3: For running test use python manage.py test

step 4: For running this project run python manage.py runserver


Api Documentation:
1. User createtion:
   request type : post
   url: '/api/user-management/create'
   body: {
      username: "username",
      email : "email@gmail.com"
      password : "123456"
   }
2. Token :
   request type : "get"
   url : "/api/user-management/token"
3. Refresh token :
   request type : post
   url : "/api/token/refresh"
         
4. Averate temperature:
   request type : get
   url : '/api/avg-temperature'
   Bearer token required
   
5. Travel recomendation
   request type: get
   url : '/api/travel-recommendation?friend_lat=23.7115253&friend_lon=90.4111451&dest_lat=24.937533&dest_lon=89.937775&travel_date=2024-12-12'
   Bearer token required
   

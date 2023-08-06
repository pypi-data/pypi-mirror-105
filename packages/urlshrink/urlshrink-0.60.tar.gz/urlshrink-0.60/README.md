# urlshrink
an open source python based url shortener
- [X] sqlite database
- [X] hashids 
- [X] redirection
- [X] hit counting
- [X] copy buttons
- [X] delete button
- [X] qr codes
- [X] options
  - [X] key / password or public deletable
  - [X] gets destroyed after x timeunits
- [X] db cleansing after X days so the hashids don't get too long 
- [X] sqlmap --risk 3 --level 5 nothing found
- [X] cookie info
- [X] made by
  
- [X] hashed fields
    - username
    - password
- [X] encrypted fields
    - using Argon2
    - url (if password for it is specified)
  
- [ ] users
  - [X] registration
    - [X] generated username
      
  - [X] add shortened url to currently logged-in user instance
  - [ ] share urls between users
    - [ ] access groups
      
  - [ ] free version:
    - [ ] delete user after x months without login
    - [ ] delete url after x years or x months without usage
    - [ ] user can only hold N shortened urls
  - [ ] paid version:
    - [ ] encryption_level + N
    - [ ] user and the users urls do not get deleted
    - [ ] user can hold {CALCULATE_ME} shortened urls
    
- [ ] sharing via platforms
- [ ] statistics
- [ ] also accept torrent, ftp, ssh, etc. urls
    - [ ] detect protocol and show label
        - some protocols can be dangerous
        - add notification for dangerous urls
  
### stuff that was originally planned but won't be done
- [ ] cli client (useless)
- [ ] api for android app (useless)
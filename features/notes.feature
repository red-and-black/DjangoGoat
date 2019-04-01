Feature: Notes

  Scenario Outline: Write a note
      Given I'm on the login page
       When I enter valid credentials "<username>" and "<password>" and push the login button
       Then I'm logged in
        And I see the dashboard
       When I click 'start a conversation'
       Then I see the write note form
       When I write a note to "<friend>" with "<content>"
       Then I see the dashboard
        And I see the new note with "<content>"

    Examples: Users
     | username         | password   |friend                  | content                       |
     | TestyMcFirstson  | Appletr33! | ThriceVonTesterbergIII | Hi Thrice, how are things?    |
     | TestrikDeuce     | Appletr33! | TestyMcFirstson        | Tap tap, is this thing on?    |
     | ImBaaaaad        | Appletr33! | NaughtyGoat            | I think its time for mischief |


  Scenario Outline: Reply to a conversation
     Given I'm on the login page
      When I enter valid credentials "<username>" and "<password>" and push the login button
      Then I'm logged in
       And I see the dashboard
       And I see a note from "<friend>"
      When I click on the note from "<friend>"
      Then I see the conversation page
      When I click on the note from "<friend>" on the conversation page
      Then I see the note page
      When I click the back button
      Then I see the conversation page
      When I write a reply to "<friend>" with "<content>"
      Then I see the conversation page
       And I see the new note with "<content>"

   Examples: Users
    | username               | password   | friend           | content                |
    | ThriceVonTesterbergIII | Appletr33! | TestyMcFirstson  | Not bad actually. You? |
    | TestyMcFirstson        | Appletr33! | TestrikDeuce     | Hey there Tesrtik      |


  Scenario: Malicious user tries to see a private note
      Given I'm on the login page
       When I enter valid credentials "ImBaaaaad" and "Appletr33!" and push the login button
       Then I'm logged in
       When I force browse to note 1
       Then I see the 404 page

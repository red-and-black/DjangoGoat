Feature: Authentication

  Scenario Outline: Create a new user and log out
      Given I'm on the sign up page
       When I create "<username>" user with "<password>" password
       Then I see the profile page
        And I'm logged in
       When I click the log out button
       Then I see the login page

    Examples: Users
     | username               | password   |
     | TestyMcFirstson        | Appletr33! |
     | TestrikDeuce           | Appletr33! |
     | ThriceVonTesterbergIII | Appletr33! |
     | ImBaaaaad              | Appletr33! |
     | NaughtyGoat            | Appletr33! |

  Scenario Outline: Update user profiles
     Given I'm on the landing page
      When I go to the login page
      When I enter valid credentials "<username>" and "<password>" and push the login button
      Then I'm logged in
       And I see the dashboard
      When I click the edit profile button
      Then I see the profile update page
      When I add a new "<bio>" and click the update button
      Then I see the profile page
      When I click the log out button
      Then I see the login page

   Examples: Users
    | username               | password   | bio                                                                              |
    | TestyMcFirstson        | Appletr33! | Easy-going goat who loves a chat. Proud Nanny to 12 grandkids.                   |
    | TestrikDeuce           | Appletr33! | A quiet soul, I'm prone to rumination. Good company if you want to chew the fat. |
    | ThriceVonTesterbergIII | Appletr33! | I'm an adventurous goat and I love to kid around. I love mountain climbing.      |
    | ImBaaaaad              | Appletr33! | Who's bad?                                                                       |
    | NaughtyGoat            | Appletr33! | 1337 h4x0r                                                                       |


  Scenario Outline: Malicious user tries to access someone elses account
    Given I'm on the landing page
      And I'm not logged in
     When I go to the login page
     When I enter invalid credentials "<username>" and "<password>" and push the login button
     Then I see an error message
      And I'm not logged in

    Examples: Users
     | username        | password   |
     | Admin           | Admin1234  |
     | TestyMcFirstson | password1! |


  Scenario Outline: User tries to create an account with a weak password
    Given I'm on the sign up page
     When I create "<username>" user with "<password>" password
     Then I'm not logged in

    Examples: Users
     | username   | password  |
     | Goaty      | goaty      |
     | Goaty      | goaty!     |
     | Goaty      | Goaty1!!   |
     | Goaty      | password   |
     | Goaty      | password1  |

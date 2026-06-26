Feature: Authentication and Collaboration

  Scenario: User can register and login
    Given the user registers with username "alice", email "alice@example.com", and password "secret"
    When the user logs in with username "alice" and password "secret"
    Then the user should receive an access token

  Scenario: User can create a task and assign it to another user
    Given the user registers with username "bob", email "bob@example.com", and password "secret"
    And the user registers with username "charlie", email "charlie@example.com", and password "secret"
    And the user logs in with username "bob" and password "secret"
    When the user creates a task with title "Buy groceries" assigned to "charlie"
    Then the task should be successfully created
    And the task should show "charlie" as the assignee
    When the user logs in with username "charlie" and password "secret"
    And the user lists tasks
    Then the list should contain the task "Buy groceries"

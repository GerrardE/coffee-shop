# Coffee Shop Full Stack

Coffee Shop is a digitally enabled cafe for students to order drinks, socialize, and study hard. Here are the features at this point:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## About the Stack

It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a completed Flask server with a SQLAlchemy module to simplify data needs.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. Just update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app.

[View the README.md within ./frontend for more details.](./frontend/README.md)

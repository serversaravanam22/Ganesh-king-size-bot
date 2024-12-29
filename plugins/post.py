from database import add_to_primary_database, fetch_from_primary_database, add_to_secondary_database, fetch_from_secondary_database

# Function to save posts to either the primary or secondary database
def save_post(post_data):
    if post_data['use_primary']:
        add_to_primary_database('posts', post_data)
    else:
        add_to_secondary_database('posts', post_data)

# Function to get posts from either the primary or secondary database
def get_post(post_id):
    if post_id % 2 == 0:  # Just an example condition
        return fetch_from_primary_database('posts', {'post_id': post_id})
    else:
        return fetch_from_secondary_database('posts', {'post_id': post_id})

# Example of handling a post command or action
def handle_new_post(post_data):
    # Some logic or filtering
    if post_data:
        save_post(post_data)
        return "Post saved successfully"
    return "Post creation failed"

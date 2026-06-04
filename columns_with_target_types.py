target_type_columns_chess = {
    'game_id': 'Int64',
    'rated': 'boolean',
    'turns': 'Int64',
    'victory_status': 'category',
    'winner': 'category',
    'time_increment': 'string',
    'white_id': 'string',
    'white_rating': 'Int64',
    'black_id': 'string',
    'black_rating': 'Int64',
    'moves': 'string',  #
    'opening_code': 'string',
    'opening_moves': 'Int64',
    'opening_fullname': 'string',
    'opening_shortname': 'string',
    'opening_variation': 'string',
}
target_type_columns_player = {
    'username': 'string',
    'display_name': 'string',
    'country': 'string',
    'registered_year': 'Int64',
    'rating_registry': 'Int64',
    'total_games_registry': 'Int64',  # category
    'account_status': 'category',
    'email_verified': 'boolean',
    'join_platform': 'string',
}


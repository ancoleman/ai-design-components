"""
Social Network Graph - Python Implementation
Demonstrates common graph database operations for a social network.
"""

from neo4j import GraphDatabase
from typing import List, Dict, Optional
from datetime import datetime, date
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SocialNetworkGraph:
    """
    Social network graph database interface using Neo4j.

    Provides methods for:
    - Friend recommendations
    - News feed generation
    - Mutual connections
    - User activity analytics
    """

    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize connection to Neo4j database.

        Args:
            uri: Neo4j connection URI (e.g., 'bolt://localhost:7687')
            user: Database username
            password: Database password
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info(f"Connected to Neo4j at {uri}")

    def close(self):
        """Close the database connection."""
        self.driver.close()
        logger.info("Database connection closed")

    def find_friends(self, user_id: str) -> List[Dict]:
        """
        Find all direct friends of a user.

        Args:
            user_id: User's unique identifier

        Returns:
            List of friend objects with name and since date
        """
        query = """
        MATCH (u:Person {id: $userId})-[r:FRIEND]-(friend)
        RETURN friend.id AS id, friend.name AS name, r.since AS since
        ORDER BY r.since DESC
        """

        with self.driver.session() as session:
            result = session.run(query, userId=user_id)
            return [dict(record) for record in result]

    def find_friends_of_friends(self, user_id: str, max_depth: int = 2) -> List[Dict]:
        """
        Find friends of friends (extended network).

        Args:
            user_id: User's unique identifier
            max_depth: Maximum degrees of separation (default: 2)

        Returns:
            List of potential connections with degree of separation
        """
        query = """
        MATCH path = (u:Person {id: $userId})-[:FRIEND*1..$maxDepth]->(connection)
        WHERE u <> connection
          AND NOT exists((u)-[:FRIEND]-(connection))
        WITH connection, length(path) AS degrees
        RETURN DISTINCT connection.id AS id,
               connection.name AS name,
               min(degrees) AS degrees_of_separation
        ORDER BY degrees_of_separation, connection.name
        LIMIT 50
        """

        with self.driver.session() as session:
            result = session.run(query, userId=user_id, maxDepth=max_depth)
            return [dict(record) for record in result]

    def find_mutual_friends(self, user1_id: str, user2_id: str) -> Dict:
        """
        Find mutual friends between two users.

        Args:
            user1_id: First user's ID
            user2_id: Second user's ID

        Returns:
            Dict with mutual friends list and count
        """
        query = """
        MATCH (u1:Person {id: $user1Id})-[:FRIEND]-(mutual)-[:FRIEND]-(u2:Person {id: $user2Id})
        RETURN collect(mutual.name) AS mutual_friends, count(mutual) AS count
        """

        with self.driver.session() as session:
            result = session.run(query, user1Id=user1_id, user2Id=user2_id)
            return dict(result.single())

    def get_friend_recommendations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Recommend potential friends based on mutual connections.

        Strategy: Friends of friends who aren't already friends, ranked by
        number of mutual friends.

        Args:
            user_id: User's unique identifier
            limit: Maximum number of recommendations

        Returns:
            List of recommended users with mutual friend count
        """
        query = """
        MATCH (u:Person {id: $userId})-[:FRIEND]->()-[:FRIEND]->(recommendation)
        WHERE NOT exists((u)-[:FRIEND]-(recommendation))
          AND u <> recommendation
        WITH recommendation, count(*) AS mutual_friends
        WHERE mutual_friends >= 2
        RETURN recommendation.id AS id,
               recommendation.name AS name,
               recommendation.bio AS bio,
               mutual_friends
        ORDER BY mutual_friends DESC
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, userId=user_id, limit=limit)
            return [dict(record) for record in result]

    def get_news_feed(self, user_id: str, limit: int = 20) -> List[Dict]:
        """
        Generate news feed for a user (posts from friends and followed users).

        Args:
            user_id: User's unique identifier
            limit: Maximum number of posts to return

        Returns:
            List of posts with author info and like count
        """
        query = """
        MATCH (u:Person {id: $userId})-[:FRIEND|FOLLOWS]->(author)-[:POSTED]->(post)
        OPTIONAL MATCH (post)<-[:LIKES]-(liker)
        WITH post, author, count(DISTINCT liker) AS like_count
        OPTIONAL MATCH (post)<-[:REPLY_TO]-(comment)
        WITH post, author, like_count, count(comment) AS comment_count
        RETURN
            post.id AS post_id,
            post.content AS content,
            post.created_at AS created_at,
            author.name AS author_name,
            author.id AS author_id,
            like_count,
            comment_count
        ORDER BY post.created_at DESC
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, userId=user_id, limit=limit)
            return [dict(record) for record in result]

    def create_friendship(self, user1_id: str, user2_id: str) -> bool:
        """
        Create a bidirectional friendship between two users.

        Args:
            user1_id: First user's ID
            user2_id: Second user's ID

        Returns:
            True if successful
        """
        query = """
        MATCH (u1:Person {id: $user1Id}), (u2:Person {id: $user2Id})
        MERGE (u1)-[:FRIEND {since: date()}]->(u2)
        MERGE (u2)-[:FRIEND {since: date()}]->(u1)
        RETURN u1.name, u2.name
        """

        with self.driver.session() as session:
            result = session.run(query, user1Id=user1_id, user2Id=user2_id)
            record = result.single()
            if record:
                logger.info(f"Created friendship: {record['u1.name']} <-> {record['u2.name']}")
                return True
            return False

    def create_post(self, user_id: str, content: str, visibility: str = 'public') -> str:
        """
        Create a new post for a user.

        Args:
            user_id: User's unique identifier
            content: Post content
            visibility: Post visibility (public, friends, private)

        Returns:
            Post ID if successful
        """
        query = """
        MATCH (u:Person {id: $userId})
        CREATE (p:Post {
            id: randomUUID(),
            content: $content,
            created_at: datetime(),
            visibility: $visibility
        })
        CREATE (u)-[:POSTED {timestamp: datetime()}]->(p)
        RETURN p.id AS post_id
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                userId=user_id,
                content=content,
                visibility=visibility
            )
            record = result.single()
            if record:
                post_id = record['post_id']
                logger.info(f"Created post {post_id} for user {user_id}")
                return post_id
            return None

    def like_post(self, user_id: str, post_id: str) -> bool:
        """
        User likes a post.

        Args:
            user_id: User's unique identifier
            post_id: Post's unique identifier

        Returns:
            True if successful
        """
        query = """
        MATCH (u:Person {id: $userId}), (p:Post {id: $postId})
        MERGE (u)-[l:LIKES {timestamp: datetime()}]->(p)
        RETURN l
        """

        with self.driver.session() as session:
            result = session.run(query, userId=user_id, postId=post_id)
            return result.single() is not None

    def get_trending_posts(self, days: int = 7, limit: int = 10) -> List[Dict]:
        """
        Find trending posts (most likes in recent period).

        Args:
            days: Number of days to look back
            limit: Maximum number of posts to return

        Returns:
            List of trending posts with like counts
        """
        query = """
        MATCH (p:Post)<-[l:LIKES]-()
        WHERE p.created_at >= datetime() - duration({days: $days})
        WITH p, count(l) AS like_count
        MATCH (author)-[:POSTED]->(p)
        RETURN
            p.id AS post_id,
            p.content AS content,
            p.created_at AS created_at,
            author.name AS author_name,
            like_count
        ORDER BY like_count DESC, p.created_at DESC
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, days=days, limit=limit)
            return [dict(record) for record in result]

    def get_user_stats(self, user_id: str) -> Dict:
        """
        Get statistics for a user (friends, posts, likes, etc.).

        Args:
            user_id: User's unique identifier

        Returns:
            Dict with user statistics
        """
        query = """
        MATCH (u:Person {id: $userId})
        OPTIONAL MATCH (u)-[:FRIEND]-(friend)
        OPTIONAL MATCH (u)-[:POSTED]->(post)
        OPTIONAL MATCH (u)-[:LIKES]->(liked)
        OPTIONAL MATCH (u)<-[:FOLLOWS]-(follower)
        OPTIONAL MATCH (u)-[:FOLLOWS]->(following)
        RETURN
            u.name AS name,
            u.joined_date AS joined_date,
            count(DISTINCT friend) AS friend_count,
            count(DISTINCT post) AS post_count,
            count(DISTINCT liked) AS likes_given,
            count(DISTINCT follower) AS follower_count,
            count(DISTINCT following) AS following_count
        """

        with self.driver.session() as session:
            result = session.run(query, userId=user_id)
            return dict(result.single())


def main():
    """Example usage of SocialNetworkGraph."""

    # Initialize connection
    graph = SocialNetworkGraph(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    try:
        # Example: Get Alice's friends
        print("\n=== Alice's Friends ===")
        friends = graph.find_friends('u1')
        for friend in friends:
            print(f"- {friend['name']} (friends since {friend['since']})")

        # Example: Get friend recommendations for Alice
        print("\n=== Friend Recommendations for Alice ===")
        recommendations = graph.get_friend_recommendations('u1', limit=5)
        for rec in recommendations:
            print(f"- {rec['name']} ({rec['mutual_friends']} mutual friends)")

        # Example: Get Alice's news feed
        print("\n=== Alice's News Feed ===")
        feed = graph.get_news_feed('u1', limit=5)
        for post in feed:
            print(f"\n{post['author_name']}: {post['content']}")
            print(f"  Likes: {post['like_count']}, Comments: {post['comment_count']}")
            print(f"  Posted: {post['created_at']}")

        # Example: Get mutual friends
        print("\n=== Mutual Friends: Alice & Charlie ===")
        mutual = graph.find_mutual_friends('u1', 'u3')
        print(f"Mutual friends: {', '.join(mutual['mutual_friends'])}")
        print(f"Count: {mutual['count']}")

        # Example: Get user stats
        print("\n=== Alice's Stats ===")
        stats = graph.get_user_stats('u1')
        print(f"Name: {stats['name']}")
        print(f"Friends: {stats['friend_count']}")
        print(f"Posts: {stats['post_count']}")
        print(f"Followers: {stats['follower_count']}")
        print(f"Following: {stats['following_count']}")

        # Example: Get trending posts
        print("\n=== Trending Posts (Last 7 Days) ===")
        trending = graph.get_trending_posts(days=7, limit=3)
        for post in trending:
            print(f"\n{post['author_name']}: {post['content']}")
            print(f"  Likes: {post['like_count']}")

    finally:
        graph.close()


if __name__ == "__main__":
    main()

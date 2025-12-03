/**
 * Social Network Graph - TypeScript Implementation
 * Demonstrates common graph database operations for a social network using Neo4j.
 */

import neo4j, { Driver, Session, Record } from 'neo4j-driver'

interface Friend {
  id: string
  name: string
  since: string
}

interface FriendRecommendation {
  id: string
  name: string
  bio: string
  mutual_friends: number
}

interface Post {
  post_id: string
  content: string
  created_at: string
  author_name: string
  author_id: string
  like_count: number
  comment_count: number
}

interface UserStats {
  name: string
  joined_date: string
  friend_count: number
  post_count: number
  likes_given: number
  follower_count: number
  following_count: number
}

interface MutualFriends {
  mutual_friends: string[]
  count: number
}

/**
 * Social network graph database interface using Neo4j.
 */
export class SocialNetworkGraph {
  private driver: Driver

  constructor(uri: string, username: string, password: string) {
    this.driver = neo4j.driver(uri, neo4j.auth.basic(username, password))
    console.log(`Connected to Neo4j at ${uri}`)
  }

  async close(): Promise<void> {
    await this.driver.close()
    console.log('Database connection closed')
  }

  /**
   * Find all direct friends of a user.
   */
  async findFriends(userId: string): Promise<Friend[]> {
    const session: Session = this.driver.session()
    try {
      const result = await session.run(
        `
        MATCH (u:Person {id: $userId})-[r:FRIEND]-(friend)
        RETURN friend.id AS id, friend.name AS name, r.since AS since
        ORDER BY r.since DESC
        `,
        { userId }
      )

      return result.records.map((record: Record) => ({
        id: record.get('id'),
        name: record.get('name'),
        since: record.get('since').toString(),
      }))
    } finally {
      await session.close()
    }
  }

  /**
   * Find friends of friends (extended network).
   */
  async findFriendsOfFriends(
    userId: string,
    maxDepth: number = 2
  ): Promise<Array<{ id: string; name: string; degrees_of_separation: number }>> {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `
        MATCH path = (u:Person {id: $userId})-[:FRIEND*1..$maxDepth]->(connection)
        WHERE u <> connection
          AND NOT exists((u)-[:FRIEND]-(connection))
        WITH connection, length(path) AS degrees
        RETURN DISTINCT connection.id AS id,
               connection.name AS name,
               min(degrees) AS degrees_of_separation
        ORDER BY degrees_of_separation, connection.name
        LIMIT 50
        `,
        { userId, maxDepth }
      )

      return result.records.map(record => ({
        id: record.get('id'),
        name: record.get('name'),
        degrees_of_separation: record.get('degrees_of_separation').toNumber(),
      }))
    } finally {
      await session.close()
    }
  }

  /**
   * Find mutual friends between two users.
   */
  async findMutualFriends(user1Id: string, user2Id: string): Promise<MutualFriends> {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `
        MATCH (u1:Person {id: $user1Id})-[:FRIEND]-(mutual)-[:FRIEND]-(u2:Person {id: $user2Id})
        RETURN collect(mutual.name) AS mutual_friends, count(mutual) AS count
        `,
        { user1Id, user2Id }
      )

      const record = result.records[0]
      return {
        mutual_friends: record.get('mutual_friends'),
        count: record.get('count').toNumber(),
      }
    } finally {
      await session.close()
    }
  }

  /**
   * Recommend potential friends based on mutual connections.
   */
  async getFriendRecommendations(
    userId: string,
    limit: number = 10
  ): Promise<FriendRecommendation[]> {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `
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
        `,
        { userId, limit }
      )

      return result.records.map(record => ({
        id: record.get('id'),
        name: record.get('name'),
        bio: record.get('bio'),
        mutual_friends: record.get('mutual_friends').toNumber(),
      }))
    } finally {
      await session.close()
    }
  }

  /**
   * Generate news feed for a user (posts from friends and followed users).
   */
  async getNewsFeed(userId: string, limit: number = 20): Promise<Post[]> {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `
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
        `,
        { userId, limit }
      )

      return result.records.map(record => ({
        post_id: record.get('post_id'),
        content: record.get('content'),
        created_at: record.get('created_at').toString(),
        author_name: record.get('author_name'),
        author_id: record.get('author_id'),
        like_count: record.get('like_count').toNumber(),
        comment_count: record.get('comment_count').toNumber(),
      }))
    } finally {
      await session.close()
    }
  }

  /**
   * Create a bidirectional friendship between two users.
   */
  async createFriendship(user1Id: string, user2Id: string): Promise<boolean> {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `
        MATCH (u1:Person {id: $user1Id}), (u2:Person {id: $user2Id})
        MERGE (u1)-[:FRIEND {since: date()}]->(u2)
        MERGE (u2)-[:FRIEND {since: date()}]->(u1)
        RETURN u1.name AS name1, u2.name AS name2
        `,
        { user1Id, user2Id }
      )

      if (result.records.length > 0) {
        const record = result.records[0]
        console.log(`Created friendship: ${record.get('name1')} <-> ${record.get('name2')}`)
        return true
      }
      return false
    } finally {
      await session.close()
    }
  }

  /**
   * Create a new post for a user.
   */
  async createPost(
    userId: string,
    content: string,
    visibility: string = 'public'
  ): Promise<string | null> {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `
        MATCH (u:Person {id: $userId})
        CREATE (p:Post {
            id: randomUUID(),
            content: $content,
            created_at: datetime(),
            visibility: $visibility
        })
        CREATE (u)-[:POSTED {timestamp: datetime()}]->(p)
        RETURN p.id AS post_id
        `,
        { userId, content, visibility }
      )

      if (result.records.length > 0) {
        const postId = result.records[0].get('post_id')
        console.log(`Created post ${postId} for user ${userId}`)
        return postId
      }
      return null
    } finally {
      await session.close()
    }
  }

  /**
   * User likes a post.
   */
  async likePost(userId: string, postId: string): Promise<boolean> {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `
        MATCH (u:Person {id: $userId}), (p:Post {id: $postId})
        MERGE (u)-[l:LIKES {timestamp: datetime()}]->(p)
        RETURN l
        `,
        { userId, postId }
      )

      return result.records.length > 0
    } finally {
      await session.close()
    }
  }

  /**
   * Find trending posts (most likes in recent period).
   */
  async getTrendingPosts(days: number = 7, limit: number = 10): Promise<Post[]> {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `
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
        `,
        { days, limit }
      )

      return result.records.map(record => ({
        post_id: record.get('post_id'),
        content: record.get('content'),
        created_at: record.get('created_at').toString(),
        author_name: record.get('author_name'),
        author_id: '',
        like_count: record.get('like_count').toNumber(),
        comment_count: 0,
      }))
    } finally {
      await session.close()
    }
  }

  /**
   * Get statistics for a user.
   */
  async getUserStats(userId: string): Promise<UserStats> {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `
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
        `,
        { userId }
      )

      const record = result.records[0]
      return {
        name: record.get('name'),
        joined_date: record.get('joined_date').toString(),
        friend_count: record.get('friend_count').toNumber(),
        post_count: record.get('post_count').toNumber(),
        likes_given: record.get('likes_given').toNumber(),
        follower_count: record.get('follower_count').toNumber(),
        following_count: record.get('following_count').toNumber(),
      }
    } finally {
      await session.close()
    }
  }
}

/**
 * Example usage
 */
async function main() {
  const graph = new SocialNetworkGraph(
    'bolt://localhost:7687',
    'neo4j',
    'password'
  )

  try {
    // Example: Get Alice's friends
    console.log('\n=== Alice\'s Friends ===')
    const friends = await graph.findFriends('u1')
    friends.forEach(friend => {
      console.log(`- ${friend.name} (friends since ${friend.since})`)
    })

    // Example: Get friend recommendations
    console.log('\n=== Friend Recommendations for Alice ===')
    const recommendations = await graph.getFriendRecommendations('u1', 5)
    recommendations.forEach(rec => {
      console.log(`- ${rec.name} (${rec.mutual_friends} mutual friends)`)
    })

    // Example: Get news feed
    console.log('\n=== Alice\'s News Feed ===')
    const feed = await graph.getNewsFeed('u1', 5)
    feed.forEach(post => {
      console.log(`\n${post.author_name}: ${post.content}`)
      console.log(`  Likes: ${post.like_count}, Comments: ${post.comment_count}`)
      console.log(`  Posted: ${post.created_at}`)
    })

    // Example: Get user stats
    console.log('\n=== Alice\'s Stats ===')
    const stats = await graph.getUserStats('u1')
    console.log(`Name: ${stats.name}`)
    console.log(`Friends: ${stats.friend_count}`)
    console.log(`Posts: ${stats.post_count}`)
    console.log(`Followers: ${stats.follower_count}`)
    console.log(`Following: ${stats.following_count}`)
  } finally {
    await graph.close()
  }
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error)
}

export default SocialNetworkGraph

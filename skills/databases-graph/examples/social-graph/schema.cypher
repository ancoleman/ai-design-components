// Social Network Graph Schema
// This schema supports a typical social network application with:
// - Users, posts, comments
// - Friend relationships
// - Follow relationships
// - Likes and interactions

// ============================================================================
// NODE TYPES
// ============================================================================

// Person nodes
// Properties: id (unique), name, email (unique), bio, joined_date
// Example: (:Person {id: 'u123', name: 'Alice', email: 'alice@example.com'})

// Post nodes
// Properties: id (unique), content, created_at, visibility
// Example: (:Post {id: 'p456', content: 'Hello world', created_at: datetime()})

// Comment nodes
// Properties: id (unique), text, created_at
// Example: (:Comment {id: 'c789', text: 'Great post!', created_at: datetime()})

// Group nodes (optional)
// Properties: id (unique), name, description, created_at
// Example: (:Group {id: 'g101', name: 'Graph Enthusiasts', description: '...'})

// ============================================================================
// RELATIONSHIP TYPES
// ============================================================================

// FRIEND (bidirectional - symmetric relationship)
// Properties: since (date when friendship started)
// Pattern: (:Person)-[:FRIEND {since: date('2020-01-15')}]->(:Person)
// Query both ways: MATCH (a)-[:FRIEND]-(b)

// FOLLOWS (directional - asymmetric relationship)
// Properties: since (date when follow started)
// Pattern: (:Person)-[:FOLLOWS {since: date('2020-01-15')}]->(:Person)

// POSTED
// Properties: timestamp (when posted)
// Pattern: (:Person)-[:POSTED {timestamp: datetime()}]->(:Post)

// COMMENTED
// Properties: timestamp
// Pattern: (:Person)-[:COMMENTED {timestamp: datetime()}]->(:Comment)

// REPLY_TO (comments can reply to posts or other comments)
// Properties: none
// Pattern: (:Comment)-[:REPLY_TO]->(:Post)
// Pattern: (:Comment)-[:REPLY_TO]->(:Comment)

// LIKES (can like posts or comments)
// Properties: timestamp
// Pattern: (:Person)-[:LIKES {timestamp: datetime()}]->(:Post)
// Pattern: (:Person)-[:LIKES {timestamp: datetime()}]->(:Comment)

// MEMBER_OF (group membership)
// Properties: joined (date), role (admin, member)
// Pattern: (:Person)-[:MEMBER_OF {joined: date(), role: 'member'}]->(:Group)

// ============================================================================
// CONSTRAINTS
// ============================================================================

// Unique constraints
CREATE CONSTRAINT person_id_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT person_email_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.email IS UNIQUE;
CREATE CONSTRAINT post_id_unique IF NOT EXISTS FOR (p:Post) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT comment_id_unique IF NOT EXISTS FOR (c:Comment) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT group_id_unique IF NOT EXISTS FOR (g:Group) REQUIRE g.id IS UNIQUE;

// ============================================================================
// INDEXES
// ============================================================================

// Indexes for frequently queried properties
CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name);
CREATE INDEX post_created_at IF NOT EXISTS FOR (p:Post) ON (p.created_at);
CREATE INDEX comment_created_at IF NOT EXISTS FOR (c:Comment) ON (c.created_at);

// Full-text search index for posts
CREATE FULLTEXT INDEX post_content_search IF NOT EXISTS FOR (p:Post) ON EACH [p.content];

// ============================================================================
// SAMPLE DATA
// ============================================================================

// Create users
CREATE (alice:Person {
  id: 'u1',
  name: 'Alice Johnson',
  email: 'alice@example.com',
  bio: 'Software engineer passionate about graphs',
  joined_date: date('2020-01-15')
});

CREATE (bob:Person {
  id: 'u2',
  name: 'Bob Smith',
  email: 'bob@example.com',
  bio: 'Data scientist and graph enthusiast',
  joined_date: date('2020-03-22')
});

CREATE (charlie:Person {
  id: 'u3',
  name: 'Charlie Davis',
  email: 'charlie@example.com',
  bio: 'Graph database consultant',
  joined_date: date('2020-05-10')
});

CREATE (diana:Person {
  id: 'u4',
  name: 'Diana Lee',
  email: 'diana@example.com',
  bio: 'Full-stack developer',
  joined_date: date('2020-07-18')
});

CREATE (eve:Person {
  id: 'u5',
  name: 'Eve Martinez',
  email: 'eve@example.com',
  bio: 'ML engineer working with knowledge graphs',
  joined_date: date('2020-09-05')
});

// Create friendships (bidirectional)
MATCH (a:Person {id: 'u1'}), (b:Person {id: 'u2'})
CREATE (a)-[:FRIEND {since: date('2020-04-01')}]->(b),
       (b)-[:FRIEND {since: date('2020-04-01')}]->(a);

MATCH (a:Person {id: 'u1'}), (c:Person {id: 'u3'})
CREATE (a)-[:FRIEND {since: date('2020-06-15')}]->(c),
       (c)-[:FRIEND {since: date('2020-06-15')}]->(a);

MATCH (b:Person {id: 'u2'}), (c:Person {id: 'u3'})
CREATE (b)-[:FRIEND {since: date('2020-07-20')}]->(c),
       (c)-[:FRIEND {since: date('2020-07-20')}]->(b);

MATCH (c:Person {id: 'u3'}), (d:Person {id: 'u4'})
CREATE (c)-[:FRIEND {since: date('2020-08-30')}]->(d),
       (d)-[:FRIEND {since: date('2020-08-30')}]->(c);

// Create follows (directional)
MATCH (a:Person {id: 'u1'}), (d:Person {id: 'u4'})
CREATE (a)-[:FOLLOWS {since: date('2020-08-01')}]->(d);

MATCH (d:Person {id: 'u4'}), (e:Person {id: 'u5'})
CREATE (d)-[:FOLLOWS {since: date('2020-10-15')}]->(e);

MATCH (e:Person {id: 'u5'}), (a:Person {id: 'u1'})
CREATE (e)-[:FOLLOWS {since: date('2020-11-01')}]->(a);

// Create posts
MATCH (a:Person {id: 'u1'})
CREATE (p1:Post {
  id: 'p1',
  content: 'Just learned about graph databases! Mind = blown 🤯',
  created_at: datetime('2025-01-01T10:30:00'),
  visibility: 'public'
}),
(a)-[:POSTED {timestamp: datetime('2025-01-01T10:30:00')}]->(p1);

MATCH (b:Person {id: 'u2'})
CREATE (p2:Post {
  id: 'p2',
  content: 'Working on a recommendation engine using Neo4j. The traversals are so elegant!',
  created_at: datetime('2025-01-02T14:15:00'),
  visibility: 'public'
}),
(b)-[:POSTED {timestamp: datetime('2025-01-02T14:15:00')}]->(p2);

MATCH (c:Person {id: 'u3'})
CREATE (p3:Post {
  id: 'p3',
  content: 'Anyone interested in a graph database meetup next week?',
  created_at: datetime('2025-01-03T09:00:00'),
  visibility: 'public'
}),
(c)-[:POSTED {timestamp: datetime('2025-01-03T09:00:00')}]->(p3);

// Create comments
MATCH (b:Person {id: 'u2'}), (p1:Post {id: 'p1'})
CREATE (c1:Comment {
  id: 'c1',
  text: 'Welcome to the graph world! Check out Neo4j GraphAcademy for great tutorials.',
  created_at: datetime('2025-01-01T11:00:00')
}),
(b)-[:COMMENTED {timestamp: datetime('2025-01-01T11:00:00')}]->(c1),
(c1)-[:REPLY_TO]->(p1);

MATCH (a:Person {id: 'u1'}), (p2:Post {id: 'p2'})
CREATE (c2:Comment {
  id: 'c2',
  text: 'I\'d love to hear more about your recommendation engine!',
  created_at: datetime('2025-01-02T15:30:00')
}),
(a)-[:COMMENTED {timestamp: datetime('2025-01-02T15:30:00')}]->(c2),
(c2)-[:REPLY_TO]->(p2);

MATCH (c:Person {id: 'u3'}), (c2:Comment {id: 'c2'})
CREATE (c3:Comment {
  id: 'c3',
  text: 'Same here! Collaborative filtering with Cypher is a game changer.',
  created_at: datetime('2025-01-02T16:00:00')
}),
(c)-[:COMMENTED {timestamp: datetime('2025-01-02T16:00:00')}]->(c3),
(c3)-[:REPLY_TO]->(c2);

// Create likes
MATCH (a:Person {id: 'u1'}), (p2:Post {id: 'p2'})
CREATE (a)-[:LIKES {timestamp: datetime('2025-01-02T14:20:00')}]->(p2);

MATCH (c:Person {id: 'u3'}), (p1:Post {id: 'p1'})
CREATE (c)-[:LIKES {timestamp: datetime('2025-01-01T12:00:00')}]->(p1);

MATCH (d:Person {id: 'u4'}), (p3:Post {id: 'p3'})
CREATE (d)-[:LIKES {timestamp: datetime('2025-01-03T10:00:00')}]->(p3);

MATCH (e:Person {id: 'u5'}), (c1:Comment {id: 'c1'})
CREATE (e)-[:LIKES {timestamp: datetime('2025-01-01T13:00:00')}]->(c1);

// Create a group
CREATE (g:Group {
  id: 'g1',
  name: 'Graph Database Enthusiasts',
  description: 'A community for people passionate about graph databases',
  created_at: date('2020-02-01')
});

// Add group memberships
MATCH (a:Person {id: 'u1'}), (g:Group {id: 'g1'})
CREATE (a)-[:MEMBER_OF {joined: date('2020-02-01'), role: 'admin'}]->(g);

MATCH (b:Person {id: 'u2'}), (g:Group {id: 'g1'})
CREATE (b)-[:MEMBER_OF {joined: date('2020-02-15'), role: 'member'}]->(g);

MATCH (c:Person {id: 'u3'}), (g:Group {id: 'g1'})
CREATE (c)-[:MEMBER_OF {joined: date('2020-03-01'), role: 'member'}]->(g);

// ============================================================================
// COMMON QUERIES
// ============================================================================

// Find friends of a user
// MATCH (u:Person {id: 'u1'})-[:FRIEND]-(friend)
// RETURN friend.name

// Find friends of friends (2 hops)
// MATCH (u:Person {id: 'u1'})-[:FRIEND*2]->(fof)
// WHERE u <> fof
// RETURN DISTINCT fof.name

// Mutual friends between two users
// MATCH (u1:Person {id: 'u1'})-[:FRIEND]-(mutual)-[:FRIEND]-(u2:Person {id: 'u2'})
// RETURN collect(mutual.name) AS mutual_friends

// Get user's feed (posts from friends and followed users)
// MATCH (u:Person {id: 'u1'})-[:FRIEND|FOLLOWS]->(author)-[:POSTED]->(post)
// OPTIONAL MATCH (post)<-[:LIKES]-(liker)
// RETURN post, author.name, count(liker) AS like_count
// ORDER BY post.created_at DESC
// LIMIT 20

// Find most active users (by post count)
// MATCH (u:Person)-[:POSTED]->(p:Post)
// RETURN u.name, count(p) AS post_count
// ORDER BY post_count DESC
// LIMIT 10

// Find trending posts (most likes in last 7 days)
// MATCH (p:Post)<-[l:LIKES]-()
// WHERE p.created_at >= datetime() - duration('P7D')
// RETURN p.content, count(l) AS like_count
// ORDER BY like_count DESC
// LIMIT 10

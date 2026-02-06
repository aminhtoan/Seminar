package com.contoso.socialapp.model;

import lombok.*;
import java.time.OffsetDateTime;
import java.util.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Post {
    private String id;
    private String username;
    private String content;
    private OffsetDateTime createdAt;
    private OffsetDateTime updatedAt;
    private int likesCount = 0;
    private int commentsCount = 0;
    private List<Comment> comments = new ArrayList<>();
    private Set<Like> likes = new HashSet<>();
}

package com.contoso.socialapp.model;

import lombok.*;
import java.io.Serializable;
import java.time.OffsetDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Like {
    private String postId;
    private String username;
    private OffsetDateTime likedAt;

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LikeId implements Serializable {
        private String postId;
        private String username;
    }
}

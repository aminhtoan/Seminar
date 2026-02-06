package com.contoso.socialapp.controller;

import org.springframework.core.io.ClassPathResource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.io.IOException;
import java.nio.file.Files;

@RestController
public class OpenApiController {
    @GetMapping(value = "/openapi.yaml", produces = "application/yaml")
    public ResponseEntity<String> getOpenApiYaml() throws IOException {
        ClassPathResource resource = new ClassPathResource("openapi.yaml");
        String yaml = Files.readString(resource.getFile().toPath());
        return ResponseEntity.ok().contentType(MediaType.valueOf("application/yaml")).body(yaml);
    }
}

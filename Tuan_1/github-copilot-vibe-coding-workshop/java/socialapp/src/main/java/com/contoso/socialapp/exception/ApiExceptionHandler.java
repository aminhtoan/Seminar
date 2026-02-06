package com.contoso.socialapp.exception;

import com.contoso.socialapp.dto.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.context.request.WebRequest;

import java.util.List;
import java.util.stream.Collectors;

@ControllerAdvice
public class ApiExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException ex) {
        List<String> details = ex.getBindingResult().getFieldErrors().stream()
                .map(error -> error.getField() + ": " + error.getDefaultMessage())
                .collect(Collectors.toList());
        ErrorResponse error = new ErrorResponse("VALIDATION_ERROR", "The request body is invalid", details);
        return ResponseEntity.badRequest().body(error);
    }

    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<ErrorResponse> handleRuntimeException(RuntimeException ex, WebRequest request) {
        String message = ex.getMessage();
        if (message != null && message.startsWith("NOT_FOUND")) {
            ErrorResponse error = new ErrorResponse("NOT_FOUND", message.replace("NOT_FOUND: ", ""), null);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
        }
        if (message != null && message.startsWith("VALIDATION_ERROR")) {
            ErrorResponse error = new ErrorResponse("VALIDATION_ERROR", message.replace("VALIDATION_ERROR: ", ""),
                    null);
            return ResponseEntity.badRequest().body(error);
        }
        ErrorResponse error = new ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred", null);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}

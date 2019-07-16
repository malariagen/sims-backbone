{{ define "backbone_env" }}
        - name: POSTGRES_DB
          valueFrom:
            configMapKeyRef:
              key: POSTGRES_DB
              name: {{ .Release.Name }}-postgres-env
        - name: POSTGRES_HOST
          valueFrom:
            configMapKeyRef:
              key: POSTGRES_HOST
              name: {{ .Release.Name }}-postgres-env
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              key: POSTGRES_PASSWORD
              name: {{ .Release.Name }}-postgres-secret-env
        - name: POSTGRES_PORT
          valueFrom:
            configMapKeyRef:
              key: POSTGRES_PORT
              name: {{ .Release.Name }}-postgres-env
        - name: POSTGRES_USER
          valueFrom:
            configMapKeyRef:
              key: POSTGRES_USER
              name: {{ .Release.Name }}-postgres-env
{{ end }}

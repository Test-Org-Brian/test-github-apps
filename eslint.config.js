import globals from 'globals'
import { defineConfig } from 'eslint/config'
import js from '@eslint/js'
import html from 'eslint-plugin-html'
import prettier from 'eslint-plugin-prettier'

export default defineConfig(
  [{
    extends: [js.configs.recommended],
    files: ["docs/*.js"],
    plugins: { prettier },
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "script",
      globals: {
        window: "readonly",
        fetch: "readonly"
      }
    },
  },
  {
    files: ["docs/*.html"],
    plugins: { html },
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "script",
    }
  }
]
)

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/460_ruleBaseSystem/dungeon_generator_frontend/', // 这里填写你的 GitHub 仓库名
})
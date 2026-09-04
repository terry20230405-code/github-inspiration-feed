import { messages, type Language } from '../i18n'

export function LanguageSwitch({ language, onChange }: { language: Language; onChange: (language: Language) => void }) {
  return <div className="language-switch" role="group" aria-label={messages[language].language}>
    <button type="button" lang="zh-CN" aria-label="切换为中文" aria-pressed={language === 'zh'} onClick={() => onChange('zh')}>中文</button>
    <span aria-hidden="true">/</span>
    <button type="button" lang="en" aria-label="Switch to English" aria-pressed={language === 'en'} onClick={() => onChange('en')}>EN</button>
  </div>
}

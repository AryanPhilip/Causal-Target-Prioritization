import { TEXT_SCALE_STORAGE_KEY, THEME_STORAGE_KEY } from "@/lib/preferences";

/**
 * Blocking script so theme + text scale from localStorage apply before paint (avoids flash).
 */
export function ThemeScript() {
  const code = `(function(){
  try{
    var t=localStorage.getItem(${JSON.stringify(THEME_STORAGE_KEY)});
    if(t==="light"||t==="dark"){document.documentElement.setAttribute("data-theme",t);}
    else{document.documentElement.removeAttribute("data-theme");}
    var s=localStorage.getItem(${JSON.stringify(TEXT_SCALE_STORAGE_KEY)});
    if(s==="large"||s==="larger"){document.documentElement.setAttribute("data-text-scale",s);}
    else{document.documentElement.removeAttribute("data-text-scale");}
  }catch(e){}
})();`;
  return <script dangerouslySetInnerHTML={{ __html: code }} />;
}

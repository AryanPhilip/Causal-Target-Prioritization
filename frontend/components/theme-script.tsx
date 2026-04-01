import { THEME_STORAGE_KEY } from "@/lib/preferences";

/**
 * Blocking script so theme from localStorage applies before paint (avoids flash).
 */
export function ThemeScript() {
  const code = `(function(){
  try{
    var t=localStorage.getItem(${JSON.stringify(THEME_STORAGE_KEY)});
    if(t==="light"||t==="dark"){document.documentElement.setAttribute("data-theme",t);}
    else{document.documentElement.removeAttribute("data-theme");}
  }catch(e){}
})();`;
  return <script dangerouslySetInnerHTML={{ __html: code }} />;
}

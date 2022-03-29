# Private Instagram Chaining
## 🔮 Uncover mutual followers of a private instagram account
illustration
## 👉 Setup & Usage
```python
# Installation
pip install tenai

# FROM YOUR TERMINAL
# Help
tenai -h/--help
# Usage
tenai -s/--session-id SESSIONID -u/--username USERNAME
# Export
tenai -s/--session-id SESSIONID -u/--username USERNAME -e/--export
# Once you logged one time with your sessionid, it is saved and use it if you don't input any

# AS LIBRARY
>>> from tenai import PrivateInstaChaining as pic
>>> info = pic(session_id=SESSIONID)
>>> info.get_data(username=USERNAME)
{"users":[user,user...],"status":"ok","is_recommend_account":False}
```
## 🗂 More
- 💡 `Tenai` comes from priva**TE** i**N**stagram ch**AI**ning.
- ⏳ Because of some pythonic part in the API response (`"sources": "[47, 11, 20]"` -> `"sources": str(list)`), this technique might be exploiting a prototype in the API that could be changed soon.
### ✅ ToDo
- [ ] [Toutatis](https://github.com/megadose/toutatis/) plugin

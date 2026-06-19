from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime

SAMPLE_URL = "https://portalsite-aiyouxi.com.cn"
CORE_KEYWORD = "爱游戏"


@dataclass
class Note:
    """单条关键词笔记"""
    keyword: str
    url: str
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def summary(self, max_len: int = 60) -> str:
        """生成简短摘要"""
        if len(self.content) <= max_len:
            return self.content
        return self.content[:max_len] + "…"


@dataclass
class KeywordNoteBook:
    """关键词笔记簿，管理多条笔记"""
    name: str = "游戏笔记"
    notes: List[Note] = field(default_factory=list)
    _default_url: str = SAMPLE_URL

    def add_note(self, keyword: str, title: str, content: str, tags: Optional[List[str]] = None,
                 url: Optional[str] = None) -> None:
        """添加一条笔记"""
        note = Note(
            keyword=keyword,
            url=url or self._default_url,
            title=title,
            content=content,
            tags=tags or []
        )
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[Note]:
        """按关键词查找笔记"""
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def find_by_tag(self, tag: str) -> List[Note]:
        """按标签查找笔记"""
        return [n for n in self.notes if tag in n.tags]

    def export_text(self, note: Note) -> str:
        """单条笔记格式化为纯文本"""
        lines = [
            f"【{note.keyword}】{note.title}",
            f"来源: {note.url}",
            f"时间: {note.created_at}",
            f"标签: {', '.join(note.tags) if note.tags else '无'}",
            "---",
            note.content,
            "",
        ]
        return "\n".join(lines)

    def format_all(self) -> str:
        """格式化所有笔记为文本（可打印/展示）"""
        if not self.notes:
            return f"📘 {self.name}：暂无笔记"
        parts = [f"📘 {self.name}（共 {len(self.notes)} 条）\n"]
        for i, note in enumerate(self.notes, 1):
            parts.append(f"[{i}] {note.keyword} — {note.title}")
        parts.append("")
        return "\n".join(parts)

    def detail_report(self) -> str:
        """生成详细报告，包含每条笔记的完整内容"""
        if not self.notes:
            return f"📘 {self.name}：暂无笔记"
        report_parts = [f"📘 {self.name} 详细报告\n"]
        for i, note in enumerate(self.notes, 1):
            report_parts.append(f"——— 笔记 {i} ———")
            report_parts.append(self.export_text(note))
        return "\n".join(report_parts)


def demo_data() -> KeywordNoteBook:
    """生成演示数据"""
    book = KeywordNoteBook(name="爱游戏笔记簿")

    book.add_note(
        keyword="爱游戏",
        title="平台简介",
        content="爱游戏是一个专注于游戏社区与资讯的门户站点，提供最新游戏动态、玩家评测与活动信息。",
        tags=["门户", "资讯"],
        url=SAMPLE_URL
    )
    book.add_note(
        keyword="游戏评测",
        title="近期热门手游评测",
        content="多款新游上线，爱游戏平台收录了来自资深玩家的真实体验报告，涵盖画面、玩法与氪金度。",
        tags=["评测", "手游"]
    )
    book.add_note(
        keyword="爱游戏",
        title="社区活动",
        content="本月爱游戏社区举办‘晒截图赢礼包’活动，玩家参与踊跃，优质作品将获得官方推荐。",
        tags=["活动", "社区"]
    )
    return book


def simple_ui(book: KeywordNoteBook) -> None:
    """简易交互（只读演示，不调用外部）"""
    print("=" * 40)
    print(book.format_all())
    print("=" * 40)
    print("\n查看详细报告？输入 'detail' 或直接回车跳过：")
    cmd = input("> ").strip().lower()
    if cmd == "detail":
        print(book.detail_report())
    else:
        print("退出演示。")


def main():
    notebook = demo_data()
    print("关键词笔记演示")
    print(f"默认 URL: {SAMPLE_URL}")
    print(f"核心关键词: {CORE_KEYWORD}")
    print(f"笔记数量: {len(notebook.notes)}\n")
    simple_ui(notebook)


if __name__ == "__main__":
    main()
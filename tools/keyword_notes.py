from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    source_url: str
    note: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def format_brief(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.created_at}] {self.keyword} ({tag_str}) — {self.note[:40]}{'...' if len(self.note) > 40 else ''}"

    def format_full(self) -> str:
        lines = []
        lines.append("=" * 50)
        lines.append(f"关键词：{self.keyword}")
        lines.append(f"来源：{self.source_url}")
        lines.append(f"创建时间：{self.created_at}")
        lines.append(f"标签：{', '.join(self.tags) if self.tags else '无'}")
        lines.append(f"笔记：{self.note}")
        lines.append("=" * 50)
        return "\n".join(lines)


@dataclass
class KeywordNotesCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def search_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def search_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag.lower() in [t.lower() for t in n.tags]]

    def list_all_brief(self) -> List[str]:
        return [note.format_brief() for note in self.notes]

    def export_all_full(self) -> str:
        return "\n\n".join(note.format_full() for note in self.notes)


def build_demo_collection() -> KeywordNotesCollection:
    collection = KeywordNotesCollection()

    note1 = KeywordNote(
        keyword="爱游戏",
        source_url="https://indexm-i-game.com.cn",
        note="这是关于爱游戏平台的笔记，记录核心玩法与用户反馈。",
        tags=["游戏", "平台", "用户体验"],
    )

    note2 = KeywordNote(
        keyword="爱游戏 新版本",
        source_url="https://indexm-i-game.com.cn/update",
        note="2025年3月发布的新版本，优化了匹配算法并增加了社交功能。",
        tags=["游戏", "更新", "社交"],
    )

    note3 = KeywordNote(
        keyword="爱游戏 活动",
        source_url="https://indexm-i-game.com.cn/events",
        note="春季庆典活动，包含限时任务和稀有道具掉落。",
        tags=["游戏", "活动", "限时"],
    )

    collection.add(note1)
    collection.add(note2)
    collection.add(note3)
    return collection


def demo_keyword_search(collection: KeywordNotesCollection) -> None:
    print("=== 关键词搜索示例：'爱游戏' ===")
    results = collection.search_by_keyword("爱游戏")
    for note in results:
        print(note.format_brief())


def demo_tag_search(collection: KeywordNotesCollection) -> None:
    print("\n=== 标签搜索示例：'活动' ===")
    results = collection.search_by_tag("活动")
    for note in results:
        print(note.format_brief())


def main() -> None:
    collection = build_demo_collection()

    print("所有笔记（简要）:")
    for brief in collection.list_all_brief():
        print(brief)

    demo_keyword_search(collection)
    demo_tag_search(collection)

    print("\n=== 导出完整笔记 ===")
    print(collection.export_all_full())


if __name__ == "__main__":
    main()
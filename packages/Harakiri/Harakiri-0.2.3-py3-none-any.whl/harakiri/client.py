from typing import Any, Dict, Optional
import aiohttp
from harakiri.model import (
    SkillData,
    AllSkillsData,
    GalleryPost,
    GalleryList,
)


class Client:
    @staticmethod
    async def get(path: str, params: Optional[Dict[str, Any]] = None):
        url = "http://manjiapi.ombe.xyz" + path
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as resp:
                return await resp.json()

    async def skill_data(self, num: int) -> SkillData:
        """Get skill data corresponding to the number.

        >>> client.skill_data(0)
        {"status":200,"info": ...

        Parameters
         - `num`(int): skill number (max: 411)

        Returns
         - Class `SkillData`
        """
        return SkillData(**await self.get(f"/skill/{num}"))

    async def all_skills_data(self) -> AllSkillsData:
        """Get all skill datas.

        >>> client.add_skills_data()
        {"status":200,"skill_list":[ ...

        Parameters
         - Nope

        Returns
         - Class `AllSkillData`
        """
        return AllSkillsData(**await self.get("/skill/all"))

    async def gallery_post(self, num: int) -> GalleryPost:
        """Get post info from yoshimitsu gallery.

        >>> client.gallery_post(4749)
        {"status":200,"content":{"title": ...

        Parameters
         - `num`(int): yoshimitsu gallery post id

        Returns
         - Class `GalleryPost`
        """
        return GalleryPost(**await self.get(f"/gallery/view/{num}"))

    async def gallery_todaytip(self, page: Optional[int] = 1) -> GalleryList:
        """Get post list from yoshimitsu gallery todaytip head.

        >>> client.gallery_todaytip(1)
        {"status":200,"total":49,"lists":[ ...

        Parameters
         - `page`(int): todaytip head page

        Returns
         - Class `GalleryList`
        """
        return GalleryList(**await self.get(f"/gallery/tt/lists/{page}"))

    async def gallery_search(
        self,
        keyword: str,
        search_mode: Optional[str] = "search_subject_memo",
        page: Optional[int] = 1,
    ):
        """Get search results from the yoshimitsu gallery.

        >>> client.gallery_search("ㅇyㅇ", "search_name", 1)
        {"status":200,"total":22,"lists":[ ...

        Parameters
         - `keyword`(str): search keyword
         - `search_mode`: search mode
              - `search_subject_memo`: search by `title + content`
              - `search_subject`: search by `title`
              - `search_memo`: search by `content`
              - `search_name`: search by `writer`

        Returns
         - Class `GalleryList`
        """
        return GalleryList(
            **await self.get(
                "/gallery/search",
                params={"keyword": keyword, "search_mode": search_mode, "page": page},
            )
        )

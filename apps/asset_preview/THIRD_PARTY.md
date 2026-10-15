# Third-party attribution

The joint pivot construction and orientation adaptation in `static/app.mjs` are adapted from
ChemLab-Assets Explorer, https://github.com/mbzuai-nlp/ChemLab-Assets, commit
`a9826f99dd08c31837b2e5be9e68f55d13cfce88`. The local viewer is independently laid out;
component selection gives specific components precedence over aggregate nodes, and
the read-only public-record projection is ChemWorld-specific.

MIT License

Copyright (c) 2026 Zirui Song, Jiadong Zhang, Jiahao Zhang, Xiaojun Chang, Xiaosong Ma, Xiuying Chen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The above MIT license covers code only. Downloaded geometry, catalogs, renders and
asset metadata retain **CC BY-NC 4.0** and any applicable third-party terms in the
downloaded `LICENSE-ASSETS.md` and `NOTICE.md`. The local assets are optional and ignored
by Git; they are not relicensed under ChemWorld's MIT license.

Three.js 0.169.0 and its loader/controls are served from the existing repository vendor
directory; its license is `apps/blender_lab/static/vendor/LICENSE.three`.

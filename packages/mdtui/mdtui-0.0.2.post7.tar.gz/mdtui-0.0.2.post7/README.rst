mdtui
======

A TUI to search and download from the new MangaDex API v5.

============
Requirements
============

- ``python>=3.7``
- ``python-pip``

==================
Installation (pip)
==================
Install from PyPI with pip:

.. code-block::

    pip install mdtui

===================
Manual Installation
===================

.. code-block::

    git clone https://git.geraldwu.com/gerald/mdtui
    cd mdtui
    python setup.py install

=====
Usage
=====

Launch the program:

.. code-block::

    $ mdtui
    >

Search for a manga:

.. code-block::

    > search Azur Lane
    Title: VictimGirls (Doujinshi), ID: 2813845e-5bfc-4ad1-8e47-3624a80e98e5
    Title: Azur Lane - In Order to be a Woman Suited for the Commander, Enterprise is Doing her Best! (Doujinshi), ID: 8aabeee6-e3ac-4f7e-8d7e-9898c7a1f48f
    Title: Azure Lane - Wakarase Bache (Doujinshi), ID: b08f5f6e-e559-4cf8-88dd-5796ea6efec5
    Title: Azur Lane - Should I Add Attending You Through the Night as Part of My Duty? (Doujinshi), ID: a375c353-0e42-4088-9eae-6e2c5d28e1ea
    Title: Azur Lane - Insufficient main force to shoot ! Iron-Blood Battleship and Battle Cruiser Summary Book (Doujinshi), ID: f9a5c000-5479-4ef7-b300-9b41c16a7f68
    Title: Azur Lane - Today, These Twin Hills Will Once More Be The Death Of Me (Doujinshi), ID: 6206645c-2c3e-409e-b988-5cd11e358b66
    Title: Azur Lane - You Didn&rsquo;t Tell Us You Were Getting a Retrofit, Z23! (Doujinshi), ID: a4d2b68c-35da-48c7-8185-d488b02c8608
    Title: Azure Lane - Junai Illustrious, ID: 97a83d5a-6b5e-4c94-8481-192331455a09
    Title: Azur Lane - The Older Sister whose Younger Sister is the Best at Everything (Doujinshi), ID: fb83a522-f654-4b00-b048-a06ad8e57c55
    Title: Azur Lane - Mukakin Shirei ni Yubiwa o Kawaseru Saigo no Houhou 5 (Doujinshi), ID: 254734f6-6de5-4a2d-9976-daf72610a732

Get chapters of a manga:

.. code-block::

    > chapters 8aabeee6-e3ac-4f7e-8d7e-9898c7a1f48f
    Chapter 4, ID: 4af0b34a-c2c5-483c-962c-ab385478ff48
    Chapter 3, ID: 549edbc3-78b7-42ee-b26a-973d5736ca51
    Chapter 2, ID: 58e64b6c-09a4-439b-8143-286243d83db9
    Chapter 4.5, ID: c0fb1084-3c27-48bc-8df3-1410b9158661
    Chapter 1, ID: efd28443-9d79-4568-b6d6-1155553a2bfe

Download chapter:

.. code-block::

    > get 4af0b34a-c2c5-483c-962c-ab385478ff48
    Downloading https://78rc8b5jajj12.fv8vk1kx3j9be.mangadex.network:443/[...]
    (Attempt 1 out of 6)
    [...]

=======
Roadmap
=======

- [ ] More user-friendly UI
- [ ] User-configurable delay and attempt limit for downloads
- [ ] Account login
- [ ] Better download directory structure
- [ ] Better REPL
- [ ] Allow for different download formats
- [ ] Write actual tests

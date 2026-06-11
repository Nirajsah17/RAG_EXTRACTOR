def chunk_with_headings(nodes, chunk_size=1000, overlap=150):

    chunks = []

    current_heading = None
    buffer = []
    size = 0

    for node in nodes:

        text = node.text.strip()
        if not text:
            continue

        is_heading = node.metadata.get("is_heading", False)

        # 🔥 heading flush
        if is_heading:

            if buffer:
                chunks.append({
                    "text": "\n".join(buffer),
                    "metadata": {
                        "heading": current_heading,
                        "page": node.page,
                        "source": node.doc_id
                    }
                })

            current_heading = text
            buffer = [text]
            size = len(text)
            continue

        # 🔥 chunk size limit
        if size + len(text) > chunk_size:

            chunks.append({
                "text": "\n".join(buffer),
                "metadata": {
                    "heading": current_heading,
                    "page": node.page,
                    "source": node.doc_id
                }
            })

            # overlap
            buffer = [buffer[-1], text]
            size = len(buffer[-1]) + len(text)

        else:
            buffer.append(text)
            size += len(text)

    # last chunk
    if buffer:
        chunks.append({
            "text": "\n".join(buffer),
            "metadata": {
                "heading": current_heading,
                "page": nodes[-1].page,
                "source": nodes[-1].doc_id
            }
        })

    return chunks
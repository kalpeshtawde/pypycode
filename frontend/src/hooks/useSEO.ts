import { useEffect } from "react";
import {
  updateMetaTags,
  updateStructuredData,
  SEOMetadata,
  StructuredData,
} from "../utils/seo";

export const useSEO = (metadata: SEOMetadata, structuredData?: StructuredData) => {
  useEffect(() => {
    updateMetaTags(metadata);
    
    if (structuredData) {
      updateStructuredData(structuredData);
    }

    // Scroll to top
    window.scrollTo(0, 0);
  }, [metadata, structuredData]);
};
